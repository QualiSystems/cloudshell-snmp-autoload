from logging import Logger

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.service.port_services.port_service_interface import (
    PortAttributesServiceInterface,
)


class PortDuplex(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        self._snmp = snmp_service
        self._logger = logger
        self._duplex_table = {}
        self._duplex_snmp_table = {}

    def load_snmp_tables(self):
        self._duplex_snmp_table = self._snmp.get_multiple_columns(
            port_constants.PORT_DUPLEX_TABLE
        )

    def _convert_duplex_table(self):
        for duplex_data in self._duplex_snmp_table.values():
            port_index = duplex_data.get(port_constants.PORT_DUPLEX_INDEX)
            if not port_index:
                continue
            port_duplex = duplex_data.get(port_constants.PORT_DUPLEX_DATA)
            self._duplex_table[port_index] = "Half"
            if port_duplex and "full" in port_duplex.lower():
                self._duplex_table[port_index] = "Full"

    def set_port_attributes(self, port_object):
        port_object.duplex = self._duplex_table.get(
            port_object.relative_address.native_index
        )

    def get_duplex_by_port_index(self, port_index):
        return self._duplex_table.get(port_index)
