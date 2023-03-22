import re
from logging import Logger

from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.services.port_table import PortsTable
from cloudshell.snmp.autoload.snmp.tables.snmp_port_mapping_table import (
    SnmpPortMappingTable,
)


class PortMappingService:
    PORT_NAME_PATTERN = re.compile(r"((\d+-).+)")
    PORT_NAME_SECONDARY_PATTERN = re.compile(r"\d+")

    def __init__(
        self,
        logger: Logger,
        port_snmp_mapping_table: SnmpPortMappingTable,
        physical_table: PhysicalTable,
        port_table: PortsTable,
    ):
        self._logger = logger
        self.port_mapping = port_snmp_mapping_table
        self._physical_table = physical_table
        self._port_table = port_table
        self._physical_port_dict = {}
        self._physical_port_ids_dict = {}
        self._get_physical_ports()

    def _get_physical_ports(self):
        for port_id in self._physical_table.physical_ports_list:
            port = self._physical_table.physical_structure_table.get(port_id)
            if self._port_table.is_wrong_port(port.name) or (
                port.port_description
                and self._port_table.is_wrong_port(port.port_description)
            ):
                continue
            self._physical_port_dict[port.name.lower()] = port
            if port.port_description:
                self._physical_port_dict[port.port_description.lower()] = port

    def get_mapping(self, port, if_descr):
        if_descr = if_descr.replace("/", "-")
        entity_port = None
        if not entity_port and port.name:
            entity_port = self._get_if_port_from_physical_port_name(port.name)
        if not entity_port and if_descr:
            entity_port = self._get_if_port_from_physical_port_name(if_descr)
        self._drop_mapped_port(entity_port)

        return entity_port

    def _get_if_port_from_physical_port_name(self, port_name):
        """Get mapping with ports from port table by port name ids.

        Build mapping based on ent_alias_mapping_table if exists else build manually
        based on entPhysicalDescr <-> ifDescr mapping.

        :return: simple mapping from entPhysicalTable index to ifTable index:
        |        {entPhysicalTable index: ifTable index, ...}
        """
        port = self._physical_port_dict.get(port_name.lower())
        if port:
            return port
        for entity_name, port in self._physical_port_dict.items():
            if_table_re = None
            port_if_match = self.PORT_NAME_PATTERN.search(entity_name)
            if not port_if_match:
                port_if_re = self.PORT_NAME_SECONDARY_PATTERN.findall(entity_name)
                if port_if_re:
                    if_table_re = "-".join(port_if_re)
            else:
                if_table_re = port_if_match.group()
            if if_table_re:
                port_pattern = re.compile(
                    rf"^\S*\D*[^-]{if_table_re}(/\D+|$)", re.IGNORECASE
                )
                if port_pattern.search(port_name) and port:
                    return port

    def _drop_mapped_port(self, port):
        if port and port.name.lower() in self._physical_port_dict:
            self._physical_port_dict.pop(port.name.lower())
        if port and port.port_description in self._physical_port_dict:
            self._physical_port_dict.pop(port.port_description.lower())
