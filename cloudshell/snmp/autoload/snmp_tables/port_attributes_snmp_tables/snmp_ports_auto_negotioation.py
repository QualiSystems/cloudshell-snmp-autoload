from logging import Logger

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_service_interface import (
    PortAttributesServiceInterface,
)


class PortAutoNegotiation(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        self._snmp = snmp_service
        self._logger = logger
        self._auto_negotiation = {}
        self._snmp_auto_negotiation = {}

    def load_snmp_tables(self):
        self._snmp_auto_negotiation = self._snmp.get_table(port_constants.PORT_AUTO_NEG)

    def _convert_auto_neg_table(self):
        self._auto_negotiation = {
            k[: k.find(".")]: v.get(port_constants.PORT_AUTO_NEG.object_name)
            for k, v in self._snmp_auto_negotiation.items()
        }

    def set_port_attributes(self, port_object):
        port_object.auto_negotiation = self.get_value_by_index(
            port_object.relative_address.native_index
        )

    def get_value_by_index(self, index):
        response = "False"
        auto_neg_data = self._auto_negotiation.get(index)
        if auto_neg_data and "enabled" in auto_neg_data.safe_value.lower():
            response = "True"
        return response
