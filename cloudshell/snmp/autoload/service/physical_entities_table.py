import re

from cloudshell.snmp.autoload.domain.entity.snmp_entity_base import BaseEntity


class PhysicalTable(object):
    PORT_EXCLUDE_RE = re.compile(
        r"stack|engine|management|mgmt|null|voice|foreign|"
        r"cpu|control\s*ethernet\s*port|console\s*port",
        re.IGNORECASE,
    )

    def __init__(self, entity_table, logger, resource_model):
        self.entity_table = entity_table
        self._logger = logger
        self._resource_model = resource_model
        self._physical_structure_table = {}
        self.port_exclude_pattern = self.PORT_EXCLUDE_RE
        self.module_exclude_pattern = None
        self.power_port_exclude_pattern = None
        self.chassis_exclude_pattern = None
        self._port_dict = {}

    def set_module_exclude_pattern(self, pattern):
        self.module_exclude_pattern = pattern
        if isinstance(self.module_exclude_pattern, str):
            self.module_exclude_pattern = re.compile(pattern, re.IGNORECASE)

    def set_port_exclude_pattern(self, pattern):
        self.port_exclude_pattern = pattern
        if isinstance(self.port_exclude_pattern, str):
            self.port_exclude_pattern = re.compile(pattern, re.IGNORECASE)

    @property
    def physical_ports_table(self):
        if not self._port_dict:
            self._get_entity_table()
        return self._port_dict

    @property
    def physical_structure_table(self):
        if not self._physical_structure_table:
            self._get_entity_table()
        return self._physical_structure_table

    def _get_entity_table(self):
        """Read Entity-MIB and filter out device's structure and all it's elements.

        Like ports, modules, chassis, etc.
        :rtype: QualiMibTable
        :return: structured and filtered EntityPhysical table.
        """
        for (
            entity_index,
            entity_data,
        ) in self.entity_table.physical_structure_snmp_table.items():
            if entity_index in self._physical_structure_table:
                continue
            entity = BaseEntity(entity_index, entity_data)
            if "port" in entity.entity_class:
                if self.port_exclude_pattern:
                    if self.port_exclude_pattern.search(
                        entity.name
                    ) or self.port_exclude_pattern.search(entity.description):
                        continue
                self._add_port(entity)
            elif "powersupply" in entity.entity_class.lower():
                self._add_power_port(entity)
            elif "chassis" in entity.entity_class.lower():
                self._add_chassis(entity)

            elif "module" in entity.entity_class.lower():
                if self.module_exclude_pattern and self.module_exclude_pattern.search(
                    entity.vendor_type
                ):
                    continue
                self._add_module(entity)

    def _add_chassis(self, entity):
        chassis_object = self._resource_model.entities.Chassis(index=entity.position_id)

        chassis_object.model = entity.model
        chassis_object.serial_number = entity.serial_number
        self._logger.debug(f"Discovered a Chassis: {entity.model}")
        self._physical_structure_table[entity.index] = chassis_object
        return chassis_object

    def _add_port(self, entity):
        name = entity.name or entity.description
        if not name:
            return
        port_object = self._resource_model.entities.Port(
            index=entity.index, name=name.replace("/", "-")
        )
        port_object.port_description = entity.description
        self._logger.debug(f"Discovered a Port: {entity.model}")
        self._physical_structure_table[entity.index] = port_object
        self._port_dict[entity.index] = port_object
        return port_object

    def _add_power_port(self, entity):
        power_port_object = self._resource_model.entities.PowerPort(
            index=entity.position_id
        )
        power_port_object.model = entity.model
        power_port_object.port_description = entity.description
        power_port_object.version = entity.hw_version
        power_port_object.serial_number = entity.serial_number
        self._logger.debug(f"Discovered a Power Port: {entity.model}")
        self._physical_structure_table[entity.index] = power_port_object
        return power_port_object

    def _add_module(self, entity: BaseEntity):
        module_object = self._resource_model.entities.Module(index=entity.position_id)
        module_object.model = entity.model
        module_object.version = entity.os_version
        module_object.serial_number = entity.serial_number
        self._logger.debug(f"Discovered a Module: {entity.model}")
        self._physical_structure_table[entity.index] = module_object
        return module_object
