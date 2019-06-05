import re

from cloudshell.snmp.autoload.core.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.domain.entity.snmp_entity_struct import (
    Chassis,
    Port,
    PowerPort,
    Module,
)
from cloudshell.snmp.autoload.helper.entity_quali_mib_table import EntityQualiMibTable
from cloudshell.snmp.autoload.service.port_mapper import PortMappingService
from cloudshell.snmp.autoload.service.port_parent_validator import PortParentValidator
from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable


class Element(object):
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.position_id
        self.child_list = []
        self.parent = None

    def add_parent(self, parent):
        self.parent = parent
        parent.child_list.append(self)


class PortElement(Element):
    def __init__(self, entity, if_entity):
        super(PortElement, self).__init__(entity)
        self.if_entity = if_entity


class SnmpEntityTable(object):
    ENTITY_PORT = Port
    ENTITY_CHASSIS = Chassis
    ENTITY_MODULE = Module
    ENTITY_POWER_PORT = PowerPort

    def __init__(self, snmp_handler, logger, if_table, validate_module_id_by_port_name=False):
        self._snmp = snmp_handler
        self._logger = logger
        self._if_table_service = if_table
        self._module_tree = dict()
        self._chassis_dict = dict()
        self.port_exclude_pattern = None
        self.module_exclude_pattern = None
        self.power_port_exclude_pattern = None
        self.chassis_exclude_pattern = None
        self._raw_physical_indexes = None
        self._port_mapping_service = None
        self._port_parent_validator_service = None
        self._validate_module_id_by_port_name = validate_module_id_by_port_name

    def set_port_exclude_pattern(self, pattern):
        self.port_exclude_pattern = pattern
        if isinstance(self.port_exclude_pattern, str):
            self.port_exclude_pattern = re.compile(pattern, re.IGNORECASE)

    @property
    def port_mapping_service(self):
        if not self._port_mapping_service:
            self._port_mapping_service = PortMappingService(self._if_table_service, self._logger)
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
        if not port:
            return

        if port.if_name == '':
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

            entity = self._raw_physical_indexes.get(entity.parent_id)
            if not entity:
                continue
            if "container" in entity.entity_class.lower():
                element.id = entity.position_id
                continue
            elif "module" in entity.entity_class.lower():
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
        if self._validate_module_id_by_port_name:
            self.port_parent_validator_service.validate_port_parent_ids(port_element)

    def _load_power_port(self, entity):
        element = Element(entity)
        while element not in self._chassis_dict:
            if entity.parent_id in self._chassis_dict:
                parent = self._chassis_dict.get(entity.parent_id)
                element.add_parent(parent)
                break

            entity = self._raw_physical_indexes.get(entity.parent_id)
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
        """Read Entity-MIB and filter out device's structure and all it's elements, like ports, modules, chassis, etc.

        :rtype: QualiMibTable
        :return: structured and filtered EntityPhysical table.
        """

        self._raw_physical_indexes = EntityQualiMibTable(self._snmp)
        index_list = self._raw_physical_indexes.raw_entity_indexes
        try:
            index_list.sort(key=lambda k: int(k), reverse=True)
        except ValueError as e:
            self._logger.error("Failed to load snmp entity table!", exc_info=1)
            raise GeneralAutoloadError("Failed to load snmp entity table.")
        for key in index_list:
            entity = self._raw_physical_indexes.get(key)
            if "port" in entity.entity_class:
                if self.port_exclude_pattern:
                    invalid_port = self.port_exclude_pattern.search(
                        entity.name
                    ) or self.port_exclude_pattern.search(entity.description)
                    if invalid_port:
                        continue
                self._load_port(self.ENTITY_PORT(entity))
            elif "powersupply" in entity.entity_class:
                self._load_power_port(self.ENTITY_POWER_PORT(entity))


if __name__ == "__main__":
    from cloudshell.core.logger.qs_logger import get_qs_logger
    from cloudshell.snmp.snmp_parameters import SNMPV2Parameters
    from cloudshell.snmp.autoload.snmp_if_table import SnmpIfTable
    from cloudshell.snmp.cloudshell_snmp import Snmp

    logger = get_qs_logger()
    # ip = "192.168.105.8"
    # ip = "192.168.73.66"
    ip = "192.168.73.115"
    # ip = "192.168.105.11"
    # ip = "192.168.105.4"
    # ip = "192.168.73.142"
    # ip = "192.168.42.235"
    comm = "public"
    # comm = "private"
    # comm = "Aa123456"
    # comm = "Cisco"
    snmp_params = SNMPV2Parameters(ip, comm)
    logger.info("started")
    snmp_handler = Snmp(logger=logger, snmp_parameters=snmp_params)

    with snmp_handler.get_snmp_service() as snmp_service:
        snmp_service.load_mib_oids(
            ["CISCO-PRODUCTS-MIB", "CISCO-ENTITY-VENDORTYPE-OID-MIB"]
        )
        if_table = SnmpIfTable(logger=logger, snmp_handler=snmp_service)
        entity_table = SnmpEntityTable(logger=logger,
                                       snmp_handler=snmp_service,
                                       if_table=if_table,
                                       validate_module_id_by_port_name=True)
        entity_table.set_port_exclude_pattern(r'stack|engine|management|'
                                              r'mgmt|voice|foreign|cpu|'
                                              r'control\s*ethernet\s*port|'
                                              r'console\s*port')
        tt = entity_table.chassis_structure_dict
        print("done")
