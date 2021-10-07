import re

from cloudshell.snmp.autoload.core.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.domain.entity.snmp_entity_base import BaseEntity
from cloudshell.snmp.autoload.domain.entity.snmp_entity_element import (
    Element,
    PortElement,
)
from cloudshell.snmp.autoload.domain.entity.snmp_entity_struct import (
    Chassis,
    Module,
    Port,
    PowerPort,
)
from cloudshell.snmp.autoload.helper.entity_quali_mib_table import EntityQualiMibTable
from cloudshell.snmp.autoload.service.port_mapper import PortMappingService
from cloudshell.snmp.autoload.service.port_parent_validator import PortParentValidator


class SnmpEntityTable(object):
    ENTITY_PORT = Port
    ENTITY_CHASSIS = Chassis
    ENTITY_MODULE = Module
    ENTITY_POWER_PORT = PowerPort

    def __init__(
        self, snmp_handler, logger, if_table, validate_module_id_by_port_name=False
    ):
        self._snmp = snmp_handler
        self._logger = logger
        self._if_table_service = if_table
        self._module_tree = {}
        self._chassis_dict = {}
        self._port_dict = {}
        self.port_exclude_pattern = None
        self.module_exclude_pattern = None
        self.power_port_exclude_pattern = None
        self.chassis_exclude_pattern = None
        self._raw_physical_indexes = None
        self._port_mapping_service = None
        self._port_parent_validator_service = None
        self.validate_module_id_by_port_name = validate_module_id_by_port_name

    def set_module_exclude_pattern(self, pattern):
        self.module_exclude_pattern = pattern
        if isinstance(self.module_exclude_pattern, str):
            self.module_exclude_pattern = re.compile(pattern, re.IGNORECASE)

    def set_port_exclude_pattern(self, pattern):
        self.port_exclude_pattern = pattern
        if isinstance(self.port_exclude_pattern, str):
            self.port_exclude_pattern = re.compile(pattern, re.IGNORECASE)

    @property
    def port_mapping_service(self):
        if not self._port_mapping_service:
            self._port_mapping_service = PortMappingService(
                self._snmp, self._if_table_service, self._logger
            )
        return self._port_mapping_service

    @property
    def port_parent_validator_service(self):
        if not self._port_parent_validator_service:
            self._port_parent_validator_service = PortParentValidator(self._logger)
        return self._port_parent_validator_service

    @property
    def chassis_structure_dict(self):
        if not self._chassis_dict:
            self._get_entity_table()
        return self._chassis_dict

    def _load_port(self, entity):
        port = self.port_mapping_service.get_mapping(entity)
        if not port or port.port_name in self._port_dict:
            return

        port_element = PortElement(entity, port)
        element = port_element
        while element not in self._chassis_dict:
            if entity.parent_id in self._module_tree:
                parent = self._module_tree.get(entity.parent_id)
                element.add_parent(parent)
                break
            if entity.parent_id in self._chassis_dict:
                parent = self._chassis_dict.get(entity.parent_id)
                element.add_parent(parent)
                break

            parent_id = entity.parent_id
            # ToDo check for 0
            entity = self._raw_physical_indexes.get(parent_id)
            if not entity:
                if not parent_id == "0":
                    self._logger.debug(
                        "Failed to autoload entity with id {}".format(parent_id)
                    )
                    return
            if "container" in entity.entity_class.lower():
                element.id = entity.position_id
                continue
            elif "module" in entity.entity_class.lower():
                if self.module_exclude_pattern and self.module_exclude_pattern.search(
                    entity.vendor_type
                ):
                    continue
                parent = Element(self.ENTITY_MODULE(entity))
                self._module_tree[entity.index] = parent
            elif entity.entity_class == "chassis":
                if entity.index not in self._chassis_dict:
                    chassis = Element(self.ENTITY_CHASSIS(entity))
                    self._chassis_dict[entity.index] = chassis
                    element.add_parent(chassis)
                    break
            else:
                continue
            element.add_parent(parent)
            element = parent
        self._validate_modules_structure(port_element)
        if self.validate_module_id_by_port_name:
            self.port_parent_validator_service.validate_port_parent_ids(port_element)
        self._port_dict[port_element.if_entity.port_name] = port_element

    def _load_power_port(self, entity):
        element = Element(entity)
        while element not in self._chassis_dict:
            if entity.parent_id in self._chassis_dict:
                parent = self._chassis_dict.get(entity.parent_id)
                element.add_parent(parent)
                break

            entity = self._raw_physical_indexes.get(entity.parent_id)
            if not entity:
                return
            if "container" in entity.entity_class.lower():
                element.id = entity.position_id
                continue
            elif entity.entity_class == "chassis":
                if entity.index not in self._chassis_dict:
                    chassis = Element(self.ENTITY_CHASSIS(entity))
                    self._chassis_dict[entity.index] = chassis
                    element.add_parent(chassis)
                    break
            else:
                continue

    def _get_entity_table(self):
        """Read Entity-MIB and filter out device's structure and all it's elements.

        Like ports, modules, chassis, etc.
        :rtype: QualiMibTable
        :return: structured and filtered EntityPhysical table.
        """
        self._raw_physical_indexes = EntityQualiMibTable(self._snmp)

        index_list = self._raw_physical_indexes.raw_entity_indexes
        try:
            index_list.sort(key=lambda k: int(k.index), reverse=True)
        except ValueError:
            self._logger.error("Failed to load snmp entity table!", exc_info=1)
            raise GeneralAutoloadError("Failed to load snmp entity table.")
        for entity_index in index_list:
            entity = BaseEntity(self._snmp, entity_index)
            if "port" in entity.entity_class:
                if self.port_exclude_pattern:
                    invalid_port = self.port_exclude_pattern.search(
                        entity.name
                    ) or self.port_exclude_pattern.search(entity.description)
                    if invalid_port:
                        continue
                self._load_port(self.ENTITY_PORT(entity))
            elif "powersupply" in entity.entity_class.lower():
                self._load_power_port(self.ENTITY_POWER_PORT(entity))
            elif "chassis" in entity.entity_class.lower():
                if entity.index not in self._chassis_dict:
                    chassis = Element(self.ENTITY_CHASSIS(entity))
                    self._chassis_dict[entity.index] = chassis

    def _validate_modules_structure(self, port):
        port_parent_list = self._get_port_parent_modules_list(port)
        if len(port_parent_list) > 2:
            port_parent_list[1].child_list.append(port)
            port.parent = port_parent_list[1]

    def _get_port_parent_modules_list(self, port):
        """Get port parent modules list.

        :type port: PortElement
        """
        result = []
        entity_element = port.parent
        while entity_element and entity_element not in self._chassis_dict.values():
            result.append(entity_element)
            entity_element = entity_element.parent
        result.reverse()
        return result
