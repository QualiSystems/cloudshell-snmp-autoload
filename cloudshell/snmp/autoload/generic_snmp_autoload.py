from functools import lru_cache

from cloudshell.shell.standards.autoload_generic_models import GenericChassis
from cloudshell.snmp.autoload.exceptions.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.services.port_mapping_table import PortMappingService
from cloudshell.snmp.autoload.services.port_table import PortsTable
from cloudshell.snmp.autoload.services.system_info_table import SnmpSystemInfo
from cloudshell.snmp.autoload.snmp.helper.snmp_autoload_helper import (
    log_autoload_details,
)
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable
from cloudshell.snmp.autoload.snmp.tables.snmp_port_mapping_table import (
    SnmpPortMappingTable,
)
from cloudshell.snmp.autoload.snmp.tables.snmp_ports_table import SnmpPortsTable


class GenericSNMPAutoload:
    def __init__(self, snmp_handler, logger, resource_model):
        """Basic init with snmp handler and logger.

        :param snmp_handler: Snmp handler for general communication
        :param logger: Logger
        :param resource_model: Represents Resource Model according to a standard
        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501

        :return:
        """
        self.snmp_handler = snmp_handler
        self.logger = logger
        self.elements = {}
        self._entity_table = None
        self._port_snmp_table = None
        self._if_table = None
        self._port_table = None
        self._system_info = None
        self._resource_model = resource_model
        self._validate_module_id_by_port_name = False
        self._chassis = {}
        self._port_table_service = None
        self._physical_table_service = None
        self._port_mapping_service = None
        self._port_parent_ids_to_module_map = {}
        self._port_id_to_module_map = {}
        self._identified_ports = []

    @property
    @lru_cache()
    def system_info_service(self):
        return SnmpSystemInfo(self.snmp_handler, self.logger)

    @property
    @lru_cache()
    def port_snmp_mapping_table(self):
        return SnmpPortMappingTable(
            snmp_handler=self.snmp_handler,
            logger=self.logger,
        )

    @property
    @lru_cache()
    def snmp_physical_structure(self):
        return SnmpEntityTable(
            snmp_handler=self.snmp_handler,
            logger=self.logger,
        )

    @property
    @lru_cache()
    def port_snmp_table(self):
        return SnmpPortsTable(
            snmp_handler=self.snmp_handler,
            logger=self.logger,
        )

    @property
    def port_table_service(self):
        if not self._port_table_service:
            self._port_table_service = PortsTable(
                resource_model=self._resource_model,
                ports_snmp_table=self.port_snmp_table,
                logger=self.logger,
            )
        return self._port_table_service

    @property
    def physical_table_service(self):
        if not self._physical_table_service:
            self._physical_table_service = PhysicalTable(
                entity_table=self.snmp_physical_structure,
                logger=self.logger,
                resource_model=self._resource_model,
            )
        return self._physical_table_service

    @property
    def port_mapping_table_service(self):
        if not self._port_mapping_service:
            self._port_mapping_service = PortMappingService(
                logger=self.logger,
                port_snmp_mapping_table=self.port_snmp_mapping_table,
                physical_table=self.physical_table_service,
                port_table=self.port_table_service,
            )
        return self._port_mapping_service

    def load_mibs(self, path):
        """Loads mibs inside snmp handler."""
        self.snmp_handler.update_mib_sources(path)

    def discover(
        self,
        supported_os,
    ):
        """General entry point for autoload.

        Read device structure and attributes:
        chassis, modules, submodules, ports, port-channels and power supplies.

        :param str supported_os:
        :return: AutoLoadDetails object
        """
        self._chassis = self.physical_table_service.physical_chassis_dict
        if not self.system_info_service.is_valid_device_os(supported_os):
            raise GeneralAutoloadError("Unsupported device OS")

        self.logger.info("*" * 70)
        self.logger.info("Start SNMP discovery process .....")
        self.system_info_service.fill_attributes(self._resource_model)
        self._build_chassis()
        self._build_power_ports()
        self._build_ports_structure()
        self._get_port_channels()
        self.logger.info("SNMP discovery process finished successfully")

        autoload_details = self._resource_model.build(
            filter_empty_modules=True, use_new_unique_id=True
        )

        log_autoload_details(self.logger, autoload_details)
        return autoload_details

    def _build_power_ports(self):
        for (
            power_port_id,
            power_port,
        ) in self.physical_table_service.physical_power_ports_dict.items():
            parent_object = self.physical_table_service.get_parent_chassis(
                power_port_id
            )
            parent = self.physical_table_service.physical_chassis_dict.get(
                parent_object.index
            )
            parent.connect_power_port(power_port)

    def _add_dummy_chassis(self, chassis_id):
        """Create Dummy Chassis."""
        chassis_object: GenericChassis = self._resource_model.entities.Chassis(
            index=chassis_id
        )

        self._resource_model.connect_chassis(chassis_object)
        self._chassis.update({str(chassis_id): chassis_object})
        self.logger.info(f"Added Dummy Chassis with index {chassis_id}")

    def _build_ports_structure(self):
        """Get ports data.

        Get resource details and attributes for every port
        base on data from IF-MIB Table.
        """
        self.logger.info("Loading Ports ...")
        if self.port_table_service.ports_dict:
            if self.port_snmp_mapping_table:
                self._load_ports_based_on_mapping()

            if len(self.port_table_service.ports_dict) == len(self._identified_ports):
                return
            self._load_ports_from_if_table()

        elif self.physical_table_service.physical_ports_list:
            self._load_ports_from_physical_table()

        self.logger.info("Building Ports completed")

    def _load_ports_based_on_mapping(self):
        for (
            if_index,
            phys_port_index,
        ) in self.port_snmp_mapping_table.port_mapping_snmp_table.items():
            phys_port = self.physical_table_service.physical_structure_table.get(
                phys_port_index
            )
            if not self._is_valid_port(phys_port):
                continue
            if_port = self.port_table_service.ports_dict.get(if_index)
            port_if_entity = self.port_table_service.load_if_port(if_index)
            port_id = port_if_entity.port_id
            port_ids = port_id[: port_id.rfind("-")]
            if len(port_ids.split("-")) > 3:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(if_port)
                self._identified_ports.append(if_index)
                continue

            parent = self._attach_port_to_parent(phys_port, if_port, port_id)
            if not parent:
                continue
            self._identified_ports.append(if_index)
            if port_ids not in self._port_id_to_module_map:
                self._port_id_to_module_map[port_ids] = parent

    def _load_ports_from_if_table(self):
        for if_index, interface in self.port_table_service.ports_dict.items():
            if if_index in self._identified_ports:
                continue

            port_if_entity = self.port_table_service.load_if_port(if_index)
            sec_name = port_if_entity.if_descr_name
            port_id = port_if_entity.port_id
            port_ids = port_id[: port_id.rfind("-")]
            if len(port_id.split("-")) > 4:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(interface)
                continue
            if self.physical_table_service.physical_ports_list:
                entity_port = self.port_mapping_table_service.get_mapping(
                    interface, sec_name
                )
                if not entity_port:
                    self.logger.debug(f"No mapping found for port {interface.name}")
                elif self._is_valid_port(entity_port):
                    self._attach_port_to_parent(entity_port, interface, port_id)
                    self._port_id_to_module_map[port_ids] = parent
                    self._identified_ports.append(if_index)
                    continue
            self._guess_port_parent(if_index, interface)
            self._identified_ports.append(if_index)

    def _load_ports_from_physical_table(self):
        for phys_port in self.physical_table_service.physical_ports_list:
            parent = self.physical_table_service.get_parent_entity(
                phys_port,
            )
            if parent:
                parent.connect_port(phys_port)

    def _guess_port_parent(self, if_index, interface):
        port_if_entity = self.port_table_service.load_if_port(if_index)
        port_id = port_if_entity.port_id
        port_ids = port_id[: port_id.rfind("-")]
        parent = self.physical_table_service.get_parent_entity_by_ids(port_ids)
        if parent:
            parent.connect_port(interface)
            self._port_id_to_module_map[port_ids] = parent
        else:
            self._add_port_to_chassis(interface, port_id)

    def _is_valid_port(self, entity_port):
        result = True
        if self.port_table_service.is_wrong_port(entity_port.name):
            result = False
        if entity_port.port_description and self.port_table_service.is_wrong_port(
            entity_port.port_description
        ):
            result = False
        return result

    def _attach_port_to_parent(self, entity_port, if_port, port_id):
        parent = self.physical_table_service.get_port_parent_entity(entity_port)
        parent = self._detect_and_connect_parent(parent)
        if parent:
            if (
                len(port_id.split("-")) - len(str(parent.relative_address).split("/"))
                > 1
            ):
                parent = (
                    self.physical_table_service.generate_module(parent, port_id)
                    or parent
                )
            parent.connect_port(if_port)
            self._update_parent_ids(parent, port_id)
            return parent

    def _update_parent_ids(self, parent, port_id):
        port_ids = port_id.split("-")[:-1]
        parent_ids = str(parent.relative_address).split("/")
        relative_address = parent.relative_address
        chassis = parent_ids[0].replace("CH", "")
        if len(parent_ids) > 2:
            port_ids_list = port_ids[1:]
            if len(port_ids_list) > 2:
                port_ids_list = port_ids_list[:-1]
            port_ids_reverse = port_ids_list
            port_ids_reverse.reverse()
            for module_id in port_ids_reverse:
                relative_address.native_index = module_id
                relative_address = relative_address.parent_node
        elif len(parent_ids) == 2 and len(port_ids) > 1:
            if chassis == port_ids[0]:
                parent.relative_address.native_index = port_ids[1]
                return
            else:
                parent.relative_address.native_index = port_ids[0]

    def _detect_and_connect_parent(self, entity):
        parent = self.physical_table_service.get_parent_entity(entity)
        if parent and entity not in parent.extract_sub_resources():
            if "module" in parent.name.lower():
                new_entity = self._resource_model.entities.SubModule(
                    entity.relative_address.native_index
                )
                new_entity.serial_number = parent.serial_number
                new_entity.model = parent.model
                new_entity.version = parent.version
                entity = new_entity

            entity.relative_address.parent_node = parent.relative_address
            parent.extract_sub_resources().append(entity)
            if parent in self.physical_table_service.physical_chassis_dict.values():
                return entity
            self._detect_and_connect_parent(parent)
        return entity

    def _add_port_to_chassis(self, interface, port_id):
        """Add port to chassis."""
        parent_element = None
        if len(self._chassis) > 1:
            if port_id:
                chassis_id = port_id.split("/")[0]
                parent_element = self._chassis.get(chassis_id, None)
        if not parent_element:
            if not self._chassis:
                chassis_id = "0"
                self._add_dummy_chassis(chassis_id)

        parent_element = next(iter(self._chassis.values()))
        parent_element.connect_port(interface)

    def _build_chassis(self):
        """Get Chassis element attributes.

        :type dict<str, cloudshell.snmp.autoload.snmp_entity_table.Element> chassis:
        """
        self.logger.debug("Building Chassis")
        for (
            chassis_object
        ) in self.physical_table_service.physical_chassis_dict.values():

            if chassis_object:
                self._resource_model.connect_chassis(chassis_object)
                self.logger.info(f"Added {chassis_object.model} Chassis")

    def _get_port_channels(self):
        """Get all port channels and set attributes for them.

        :return:
        Get resource details and attributes for every port
        base on data from IF-MIB Table.
        """
        if not self.port_table_service.port_channels_dict:
            return
        self.logger.info("Building Port Channels")
        for port_channel in self.port_table_service.port_channels_dict.values():
            self._resource_model.connect_port_channel(port_channel)
            self.logger.info(f"Added {port_channel.name}")

        self.logger.info("Building Port Channels completed")
