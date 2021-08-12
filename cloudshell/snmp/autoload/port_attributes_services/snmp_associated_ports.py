from collections import defaultdict
from logging import Logger

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.port_attributes_services.port_service_interface import (
    PortAttributesServiceInterface,
)


class PortChannelsAssociatedPorts(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        self._snmp_service = snmp_service
        self._logger = logger
        self._associated_ports = defaultdict(list)
        self._snmp_associated_ports = {}

    def load_snmp_tables(self):
        self._snmp_associated_ports = self._snmp_service.get_table(
            port_constants.PORT_CHANNEL_TABLE
        )

    def _convert_associated_ports(self):
        for index, data in self._snmp_associated_ports.items():
            port_channel_id = data.get(port_constants.PORT_CHANNEL_TABLE.object_name)
            if port_channel_id and port_channel_id.safe_value:
                self._associated_ports[port_channel_id.safe_value].append(index)

    def set_port_attributes(self, port_index):
        return self._associated_ports.get(port_index)
