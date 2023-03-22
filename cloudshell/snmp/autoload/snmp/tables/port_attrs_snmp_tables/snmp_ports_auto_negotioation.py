from logging import Logger
from threading import Thread

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_service_interface import (
    PortAttributesServiceInterface,
)


class PortAutoNegotiation(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        super().__init__(snmp_service, logger)
        self._snmp = snmp_service
        self._logger = logger
        self._auto_negotiation = {}
        self._snmp_auto_negotiation = {}

    def load_snmp_table(self):
        self._snmp_auto_negotiation = self._snmp.get_table(port_constants.PORT_AUTO_NEG)
        if self._snmp_auto_negotiation:
            thread = Thread(
                target=self._convert_auto_neg_table, name="Auto Negotiation converter"
            )
            thread.start()
            self._thread_list.append(thread)

    def _convert_auto_neg_table(self):
        self._auto_negotiation = {
            k[: k.find(".")]: v.get(port_constants.PORT_AUTO_NEG.object_name)
            for k, v in self._snmp_auto_negotiation.items()
        }

    def get_value_by_index(self, index):
        [thread.join() for thread in self._thread_list]
        response = "False"
        auto_neg_data = self._auto_negotiation.get(index)
        if auto_neg_data and "enabled" in auto_neg_data.safe_value.lower():
            response = "True"
        return response
