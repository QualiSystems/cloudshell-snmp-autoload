from logging import Logger
from threading import Thread

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_service_interface import (
    PortAttributesServiceInterface,
)


class PortDuplex(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        super().__init__(snmp_service, logger)
        self._snmp = snmp_service
        self._logger = logger
        self._duplex_table = {}
        self._duplex_snmp_table = {}

    def load_snmp_table(self):
        self._duplex_snmp_table = self._snmp.get_multiple_columns(
            port_constants.PORT_DUPLEX_TABLE
        )
        if self._duplex_snmp_table:
            thread = Thread(target=self._convert_duplex_table, name="Duplex converter")
            thread.start()
            self._thread_list.append(thread)

    def _convert_duplex_table(self):
        for duplex_data in self._duplex_snmp_table.values():
            port_index = duplex_data.get(port_constants.PORT_DUPLEX_INDEX.object_name)
            if not port_index:
                continue
            port_duplex = duplex_data.get(port_constants.PORT_DUPLEX_DATA.object_name)
            self._duplex_table[port_index.safe_value] = "Half"
            if port_duplex and "full" in port_duplex.safe_value.lower():
                self._duplex_table[port_index] = "Full"

    def get_duplex_by_port_index(self, port_index):
        [thread.join() for thread in self._thread_list]
        return self._duplex_table.get(port_index)
