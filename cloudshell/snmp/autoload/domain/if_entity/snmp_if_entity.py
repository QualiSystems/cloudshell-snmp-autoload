from cloudshell.snmp.autoload.constants.port_constants import PORT_NAME, PORT_DESCRIPTION


class SnmpIfEntity(object):
    def __init__(self, snmp_handler, logger, port_name_response, port_attributes_snmp_tables):
        self.if_index = port_name_response.index
        self._snmp = snmp_handler
        self._port_attributes_snmp_tables = port_attributes_snmp_tables
        self._logger = logger
        self._ipv4 = None
        self._ipv6 = None
        self._if_alias = None
        self._if_name = port_name_response

    @property
    def if_name(self):
        if not self._if_name:
            self._if_name = self._snmp.get_property(PORT_NAME.get_snmp_mib_oid(self.if_index)).value or ""
        return self._if_name

    @property
    def if_port_description(self):
        if not self._if_alias:
            self._if_alias = self._snmp.get_property(PORT_DESCRIPTION.get_snmp_mib_oid(self.if_index)).value or ""
        return self._if_alias

    @property
    def ipv4_address(self):
        if not self._ipv4:
            self._ipv4 = self._get_ipv4() or ""
        return self._ipv4

    @property
    def ipv6_address(self):
        if not self._ipv6:
            self._ipv6 = self._get_ipv6() or ""
        return self._ipv6

    def _get_ipv4(self):
        """Get IPv4 address details for provided port

        :return str IPv4 Address
        """

        if self._port_attributes_snmp_tables.ip_v4_table:
            for key, value in self._port_attributes_snmp_tables.ip_v4_table.iteritems():
                if_index = value.get("ipAdEntIfIndex")
                if if_index and int(if_index.value) == self.if_index:
                    return key

    def _get_ipv6(self):
        """Get IPv6 address details for provided port

        :return str IPv6 Address
        """

        if self._port_attributes_snmp_tables.ip_v6_table:
            for key, value in self._port_attributes_snmp_tables.ip_v6_table.iteritems():
                if_index = value.get("ipv6IfIndex")
                if if_index and int(if_index.value) == self.if_index:
                    return key
