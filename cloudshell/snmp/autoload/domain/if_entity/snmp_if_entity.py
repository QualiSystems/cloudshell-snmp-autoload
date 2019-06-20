from ipaddress import IPv4Address, IPv6Address

from cloudshell.snmp.autoload.constants.port_constants import PORT_NAME, PORT_DESCRIPTION, PORT_DESCR_NAME


class SnmpIfEntity(object):
    def __init__(self, snmp_handler, logger, port_name_response, port_attributes_snmp_tables):
        self.if_index = port_name_response.index
        self._snmp = snmp_handler
        self._port_attributes_snmp_tables = port_attributes_snmp_tables
        self._logger = logger
        self._ipv4 = None
        self._ipv6 = None
        self._if_alias = None
        self._if_name = None
        self._if_descr_name = None
        if port_name_response.mib_id == PORT_DESCR_NAME.mib_id:
            self._if_descr_name = port_name_response.safe_value
        else:
            self._if_name = port_name_response
        self._ips_list = None

    @property
    def if_name(self):
        if not self._if_name:
            self._if_name = self._snmp.get_property(PORT_NAME.get_snmp_mib_oid(self.if_index)).safe_value
        return self._if_name

    @property
    def if_descr_name(self):
        if not self._if_descr_name:
            self._if_descr_name = self._snmp.get_property(PORT_DESCR_NAME.get_snmp_mib_oid(self.if_index)).safe_value
        return self._if_descr_name

    @property
    def if_port_description(self):
        if not self._if_alias:
            self._if_alias = self._snmp.get_property(PORT_DESCRIPTION.get_snmp_mib_oid(self.if_index)).safe_value
        return self._if_alias

    @property
    def ipv4_address(self):
        if not self._ipv4:
            if self._ips_list is None:
                self._get_ip()
            self._ipv4 = self._get_ipv4() or ""
        return self._ipv4

    @property
    def ipv6_address(self):
        if not self._ipv6:
            if self._ips_list is None:
                self._get_ip()
            self._ipv6 = self._get_ipv6() or ""
        return self._ipv6

    def _get_ip(self):
        self._ips_list = [x for x in self._port_attributes_snmp_tables.ip_mixed_list if x.safe_value == self.if_index]
        for ip in self._ips_list:
            index = ip.index.replace("'", "")
            if index.startswith("ipv6"):
                try:
                    ipv6 = IPv6Address((index.replace("ipv6.0x", "")).decode("hex"))
                except:
                    ipv6 = ""
                self._ipv6 = ipv6
            elif index.startswith("ipv4"):
                try:
                    ipv4 = IPv4Address((index.replace("ipv4.0x", "")).decode("hex"))
                except:
                    ipv4 = ""
                self._ipv4 = ipv4

    def _get_ipv4(self):
        """Get IPv4 address details for provided port

        :return str IPv4 Address
        """

        if self._port_attributes_snmp_tables.ip_v4_old_list:
            for snmp_response in self._port_attributes_snmp_tables.ip_v4_old_list:
                if snmp_response.safe_value and snmp_response.safe_value == self.if_index:
                    return snmp_response.index

    def _get_ipv6(self):
        """Get IPv6 address details for provided port

        :return str IPv6 Address
        """

        if self._port_attributes_snmp_tables.ip_v6_list:
            for snmp_response in self._port_attributes_snmp_tables.ip_v6_list:
                if snmp_response.safe_value and snmp_response.index.startswith("{}.".format(self.if_index)):
                    return snmp_response.index.replace("{}.".format(self.if_index), "")
