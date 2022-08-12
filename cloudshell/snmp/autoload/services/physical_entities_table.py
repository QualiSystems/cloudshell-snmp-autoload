import re
from collections import defaultdict
from logging import Logger

from cloudshell.snmp.autoload.snmp.helper.snmp_entity_base import BaseEntity
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable


class PhysicalTable:
    MODULE_EXCLUDE_LIST = ["fan", "cpu"]
    MODULE_TO_CONTAINER_LIST = []

    def __init__(self, entity_table: SnmpEntityTable, logger: Logger, resource_model):
        self.entity_table = entity_table
        self._logger = logger
        self._resource_model = resource_model
        self._physical_structure_table = {}
        self._module_exclude_pattern = None
        self.power_port_exclude_pattern = None
        self.chassis_exclude_pattern = None
        self._port_list = []
        self._power_port_dict = {}
        self._chassis_dict = {}
        self._modules_dict = {}
        self._port_parent_dict = {}
        self._modules_hierarchy_dict = defaultdict(list)
        self._chassis_ids_dict = {}

    @property
    def module_exclude_pattern(self):
        pattern = "|".join(self.MODULE_EXCLUDE_LIST)
        return re.compile(pattern, re.IGNORECASE)

    @property
    def physical_ports_list(self):
        if not self._port_list:
            self._get_entity_table()
        return self._port_list

    @property
    def physical_power_ports_dict(self):
        if not self._power_port_dict:
            self._get_entity_table()
        return self._power_port_dict

    @property
    def physical_modules_ids_dict(self):
        if not self._modules_dict:
            self._get_entity_table()

        if not self._modules_hierarchy_dict:
            indexes = list(self._modules_dict.keys())
            indexes.sort()
            indexes.reverse()
            for module_index in indexes:
                ids = self._build_module_ids(module_index)
                module = self.physical_structure_table.get(module_index)
                self._modules_hierarchy_dict[ids].append(module)
        return self._modules_hierarchy_dict

    @property
    def physical_chassis_dict(self):
        if not self._chassis_dict:
            self._get_entity_table()
        return self._chassis_dict

    @property
    def physical_structure_table(self):
        if not self._physical_structure_table:
            self._get_entity_table()
        return self._physical_structure_table

    def _build_module_ids(self, entity_id):
        module_ids = []
        while entity_id:
            module = self.physical_structure_table.get(entity_id)
            module_ids.append(module.relative_address.native_index)
            entity_id = self._modules_dict.get(entity_id)
        module_ids.reverse()
        return "-".join(module_ids)

    def _get_entity_table(self):
        """Read Entity-MIB and filter out device's structure and all it's elements.

        Like ports, modules, chassis, etc.
        :rtype: QualiMibTable
        :return: structured and filtered EntityPhysical table.
        """
        for entity_index in self.entity_table.physical_structure_snmp_table:
            if entity_index in self._physical_structure_table:
                continue
            self._add_entity(entity_index)

    def load_entity(self, entity_index) -> BaseEntity:
        entity_data = self.entity_table.physical_structure_snmp_table.get(entity_index)
        return BaseEntity(entity_index, entity_data)

    def _add_entity(self, entity_index):
        if entity_index not in self.entity_table.physical_structure_table:
            return
        entity = self.load_entity(entity_index)
        if "port" in entity.entity_class:
            self._add_port(entity)
        elif "powersupply" in entity.entity_class.lower():
            self._add_power_port(entity)
        elif "chassis" in entity.entity_class.lower():
            self._add_chassis(entity)
        elif "module" in entity.entity_class.lower():
            self._add_module(entity)

    def _add_chassis(self, entity):
        index = "0" if entity.position_id == "-1" else entity.position_id
        chassis_object = self._resource_model.entities.Chassis(index=index)

        chassis_object.model = entity.model
        chassis_object.serial_number = entity.serial_number
        duplicate_chassis = next(
            (
                obj
                for obj in self._chassis_dict.values()
                if obj.serial_number == chassis_object.serial_number
                and obj.model == chassis_object.model
            ),
            None,
        )
        if duplicate_chassis:
            chassis_object = duplicate_chassis

        self._logger.debug(f"Discovered a Chassis: {entity.model}")
        self._chassis_dict[entity.index] = chassis_object
        self._physical_structure_table[entity.index] = chassis_object
        self._chassis_ids_dict[index] = chassis_object

    def _add_port(self, entity):
        name = entity.name or entity.description
        if not name:
            return
        port_object = self._resource_model.entities.Port(
            index=entity.index, name=name.replace("/", "-")
        )
        parent_module = self._find_parent_module(entity.index)
        port_object.port_description = entity.description
        self._logger.debug(f"Discovered a Port: {entity.model}")
        self._physical_structure_table[entity.index] = port_object
        self._port_list.append(entity.index)
        self._port_parent_dict[entity.index] = parent_module.index

    def _add_power_port(self, entity):
        power_port_object = self._resource_model.entities.PowerPort(
            index=entity.position_id
        )
        power_port_object.model = entity.model
        power_port_object.port_description = entity.description
        power_port_object.version = entity.hw_version
        power_port_object.serial_number = entity.serial_number
        self._logger.debug(f"Discovered a Power Port: {entity.model}")
        self._power_port_dict[entity.index] = power_port_object

    def _find_parent_containers(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        parent = self.load_entity(parent_index)
        if (
            parent.entity_class in ["container", "backplane"]
            or self.module_exclude_pattern.search(parent.vendor_type)
            or "port" in parent.entity_class
        ):
            entity = self._find_parent_containers(parent_index)
            return entity if entity else parent

    def _find_parent_module(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        if not parent_index:
            raise Exception("Error loading parent entity")
        parent = self.load_entity(parent_index)
        if not parent.entity_row_response:
            return
        if "module" in parent.entity_class and not self.module_exclude_pattern.search(
            parent.vendor_type
        ):
            return parent
        elif "chassis" in parent.entity_class:
            return parent
        else:
            return self._find_parent_module(parent_index)

    def _add_module(self, entity: BaseEntity):
        if self.module_exclude_pattern and self.module_exclude_pattern.search(
            entity.vendor_type
        ):
            return

        position_id = entity.position_id
        parent_container = self._find_parent_containers(entity.index)
        parent_module_index = entity.parent_id
        if parent_container:
            position_id = parent_container.position_id
            parent_module_index = self.entity_table.physical_structure_table.get(
                parent_container.index
            )

        module_object = self._resource_model.entities.Module(index=position_id)
        module_object.model = entity.model
        module_object.version = entity.os_version
        module_object.serial_number = entity.serial_number
        self._physical_structure_table[entity.index] = module_object
        self._logger.debug(f"Discovered a Module: {entity.model}")
        self._modules_dict[entity.index] = parent_module_index

    def get_parent_chassis(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        if not parent_index:
            raise Exception("Error loading parent entity")
        parent = self.load_entity(parent_index)
        if "chassis" in parent.entity_class:
            return parent
        else:
            return self.get_parent_chassis(parent_index)

    def get_port_parent_entity(self, entity_port):
        port_id = entity_port.relative_address.native_index
        parent_entity = self._find_parent_module(port_id)
        parent = self._physical_structure_table.get(parent_entity.index)
        return parent

    def get_parent_entity(self, entity):
        if entity in self.physical_chassis_dict.values():
            return
        entity_id = next(
            (k for k, v in self._physical_structure_table.items() if v == entity), None
        )
        parent_entity = self._find_parent_module(entity_id)
        parent = self._physical_structure_table.get(parent_entity.index)
        return parent

    def get_parent_entity_by_ids(self, port_ids):
        port_parent_id = port_ids
        if "-" in port_ids:
            port_parent_id = port_ids[: port_ids.rfind("-")]
        parent = self.physical_modules_ids_dict.get(port_parent_id)
        if not parent and len(port_ids.split("-")) < 3:
            for chassis in self._chassis_ids_dict:
                parent = self.physical_modules_ids_dict.get(
                    f"{chassis}-{port_parent_id}"
                )
                if parent:
                    return parent
        if self.physical_modules_ids_dict:
            module_id = port_ids
            ids = port_ids.split("-")
            if len(ids) == 1:
                parent = next(
                    (chassis for _, chassis in self._chassis_ids_dict.items()), None
                )
                if not parent:
                    return
            if len(ids) == 2:
                chassis, module_id = port_ids
                parent = self._chassis_ids_dict.get(chassis)
            elif len(ids) == 3:
                chassis, module_id, sub_module = port_ids
                parent = self.physical_modules_ids_dict.get(f"{chassis}-{module_id}")[
                    -1
                ]

            module_object = self._resource_model.entities.Module(index=module_id)
            self.physical_modules_ids_dict[module_id] = module_object
            module_object.relative_address.parent_node = parent.relative_address
            parent.extract_sub_resources().append(module_object)
            if module_object:
                return module_object
