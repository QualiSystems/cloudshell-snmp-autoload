import re
from copy import copy
from functools import lru_cache

from cloudshell.snmp.autoload.constants.entity_constants import ENTITY_TO_IF_ID
from cloudshell.snmp.autoload.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.port_table import PortsTable


class PortMappingService(object):
    PORT_NAME_PATTERN = re.compile(r"((\d+/).+)")
    PORT_NAME_SECONDARY_PATTERN = re.compile(r"\d+")

    def __init__(
        self, snmp, physical_table: PhysicalTable, port_table: PortsTable, logger
    ):
        self._physical_table = physical_table
        self._port_table = port_table
        self._snmp = snmp
        self._logger = logger
        self._unmapped_ports_dict = self._port_table.if_ports
        self._port_names_dict = self._port_table.port_name_to_object_map
        self._port_mapping_table = {}

    @property
    @lru_cache()
    def port_mapping_table(self):
        self._port_mapping_table = {}
        for port_id, port in self._physical_table.physical_ports_table.items():
            if_port = self.get_mapping(port)
            if if_port and if_port in self._port_mapping_table.values():
                continue
            self._port_mapping_table[port_id] = if_port
        return self._port_mapping_table

    @property
    @lru_cache()
    def port_mapping_snmp_table(self):
        port_map = {}
        for item in self._snmp.walk(ENTITY_TO_IF_ID):
            if item.safe_value:
                if_index = item.safe_value.replace("IF-MIB::ifIndex.", "")
                port = self._port_table.get_if_entity_by_index(if_index)
                if port:
                    index = item.index[: item.index.rfind(".")]
                    port_map[index] = port
                self._remove_port_from_unmapped_dict(if_index)
                self._remove_port_from_port_name_map_dict(port.name)
        return port_map

    def get_mapping(self, port_entity):
        if_port = self.port_mapping_snmp_table.get(
            port_entity.relative_address.native_index
        )
        if not if_port:
            if_port = self._get_if_port_from_physical_port_name(port_entity.name)
        if not if_port:
            if_port = self._get_if_port_from_physical_port_name(
                port_entity.port_description
            )
        if if_port:
            self._remove_port_from_unmapped_dict(if_port.relative_address.index)
            self._remove_port_from_port_name_map_dict(if_port.name)
            return if_port.relative_address.native_index
        pass

    def _get_if_port_from_physical_port_name(self, port_name):
        """Get mapping with ports from port table by port name ids.

        Build mapping based on ent_alias_mapping_table if exists else build manually
        based on entPhysicalDescr <-> ifDescr mapping.

        :return: simple mapping from entPhysicalTable index to ifTable index:
        |        {entPhysicalTable index: ifTable index, ...}
        """
        interface_id = self._port_table.port_name_to_object_map.get(port_name.lower())
        if interface_id:
            interface = self._unmapped_ports_dict.pop(interface_id)
            if interface:
                return interface
        if_table_re = None
        port_if_match = self.PORT_NAME_PATTERN.search(port_name)
        if not port_if_match:
            port_if_re = self.PORT_NAME_SECONDARY_PATTERN.findall(port_name)
            if port_if_re:
                if_table_re = "/".join(port_if_re)
        else:
            port_if_re = port_if_match.group()
            if_table_re = port_if_re
        if if_table_re:
            port_pattern = re.compile(
                r"^\S*\D*[^/]{0}(/\D+|$)".format(if_table_re), re.IGNORECASE
            )
            port_names_dict = copy(self._port_names_dict)
            for interface_name, interface_id in port_names_dict.items():
                if port_pattern.search(interface_name):
                    interface = self._unmapped_ports_dict.get(interface_id)
                    if interface:
                        return interface
                if interface_id in self._port_mapping_table.values():
                    self._remove_port_from_unmapped_dict(interface_id)
                    self._remove_port_from_port_name_map_dict(interface_name)

    def _remove_port_from_unmapped_dict(self, interface_id):
        if interface_id in self._unmapped_ports_dict:
            self._unmapped_ports_dict.pop(interface_id)

    def _remove_port_from_port_name_map_dict(self, interface_name):
        interface_id = self._port_names_dict.get(interface_name)
        if interface_id and interface_id in self._port_mapping_table.values():
            self._port_names_dict.pop(interface_name)
