from __future__ import annotations

from cloudshell.snmp.core.domain.snmp_response import SnmpResponse
from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import snmpv_v2_constants


class SnmpV2MibData:
    def __init__(self, snmp_handler: SnmpService, logger):
        self._snmp_handler = snmp_handler
        self._logger = logger
        self._sys_descr = ""
        self._sys_location = None
        self._sys_contact = None
        self._sys_object_id = None
        self._sys_name = None

    def get_system_name(self) -> SnmpResponse | None:
        if not self._sys_name:
            self._sys_name = self._snmp_handler.get_property(
                snmpv_v2_constants.SYS_NAME
            )
        return self._sys_name

    def get_system_location(self) -> SnmpResponse | None:
        if not self._sys_location:
            self._sys_location = self._snmp_handler.get_property(
                snmpv_v2_constants.SYS_LOCATION
            )
        return self._sys_location

    def get_system_contact(self) -> SnmpResponse | None:
        if not self._sys_contact:
            self._sys_contact = self._snmp_handler.get_property(
                snmpv_v2_constants.SYS_CONTACT
            )
        return self._sys_contact

    def get_system_description(self) -> str:
        if not self._sys_descr:
            self._sys_descr = self._snmp_handler.get_property(
                snmpv_v2_constants.SYS_DESCR
            ).safe_value
        return self._sys_descr

    def get_system_object_id(self) -> SnmpResponse | None:
        if not self._sys_object_id:
            self._sys_object_id = self._snmp_handler.get_property(
                snmpv_v2_constants.SYS_OBJECT_ID
            )
        return self._sys_object_id
