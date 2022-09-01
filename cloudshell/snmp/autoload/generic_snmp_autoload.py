from functools import lru_cache

from cloudshell.snmp.autoload.exceptions.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.helper.port_helper import PortHelper
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
        self._port_table_service = None
        self._physical_table_service = None
        self._port_mapping_service = None

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

    def _build_ports_structure(self):
        """Get ports data.

        Get resource details and attributes for every port
        base on data from IF-MIB Table.
        """
        port_helper = PortHelper(
            physical_table_service=self.physical_table_service,
            port_table_service=self.port_table_service,
            port_mapping_table_service=self.port_mapping_table_service,
            resource_model=self._resource_model,
            logger=self.logger,
        )
        port_helper.build_ports_structure()

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
