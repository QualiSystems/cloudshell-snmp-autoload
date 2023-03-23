from collections import defaultdict
from logging import Logger
from threading import Thread

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_service_interface import (
    PortAttributesServiceInterface,
)


class PortChannelsAssociatedPorts(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        super().__init__(snmp_service, logger)
        self._snmp_service = snmp_service
        self._logger = logger
        self._associated_ports = defaultdict(list)
        self._snmp_associated_ports = {}

    def load_snmp_table(self):
        self._snmp_associated_ports = self._snmp_service.get_table(
            port_constants.PORT_CHANNEL_TABLE
        )
        if self._snmp_associated_ports:
            thread = Thread(
                target=self._convert_associated_ports, name="Associated ports converter"
            )

            thread.start()
            self._thread_list.append(thread)

    def _convert_associated_ports(self):
        for index, data in self._snmp_associated_ports.items():
            port_channel_id = data.get(port_constants.PORT_CHANNEL_TABLE.object_name)
            if port_channel_id and port_channel_id.safe_value:
                self._associated_ports[port_channel_id.safe_value].append(index)

    def get_associated_ports(self, port_index):
        [thread.join() for thread in self._thread_list]
        return self._associated_ports.get(port_index)
