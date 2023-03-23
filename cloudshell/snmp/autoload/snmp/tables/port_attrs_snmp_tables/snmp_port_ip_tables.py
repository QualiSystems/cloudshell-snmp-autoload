from collections import defaultdict
from ipaddress import AddressValueError, IPv4Address, IPv6Address
from logging import Logger
from threading import Thread

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_service_interface import (
    PortAttributesServiceInterface,
)


class PortIPTables(PortAttributesServiceInterface):
    def __init__(self, snmp_service: SnmpService, logger: Logger):
        super().__init__(snmp_service, logger)
        self._snmp = snmp_service
        self._logger = logger
        self._ipv4_table = defaultdict(list)
        self._ipv4_snmp_table = {}
        self._ip_mixed_snmp_table = {}
        self._ipv6_table = defaultdict(list)
        self._ipv6_snmp_table = {}

    def load_snmp_table(self):
        self._ipv4_snmp_table = self._snmp.walk(port_constants.PORT_OLD_IP_INDEXES)
        if self._ipv4_snmp_table:
            self._thread_list.append(
                Thread(
                    target=self._convert_ipv4_table,
                    name="IPv4 converter",
                )
            )
        self._ip_mixed_snmp_table = self._snmp.walk(
            port_constants.PORT_MIXED_IP_INDEXES
        )
        if self._ip_mixed_snmp_table:
            self._thread_list.append(
                Thread(
                    target=self._convert_ip_mixed_table,
                    name="Mixed IPs converter",
                )
            )
        self._ipv6_snmp_table = self._snmp.walk(port_constants.PORT_MIXED_IPV6_INDEXES)
        if self._ipv6_snmp_table:
            self._thread_list.append(
                Thread(
                    target=self._convert_ipv6_table,
                    name="IPv6 converter",
                )
            )
        [thread.start() for thread in self._thread_list]

    def _convert_ipv4_table(self):
        for ip in self._ipv4_snmp_table:
            port_index = ip.safe_value
            if port_index:
                self._ipv4_table[port_index].append(ip.index)

    def _convert_ip_mixed_table(self):
        for ip in self._ip_mixed_snmp_table:
            port_index = ip.safe_value
            if not port_index:
                continue
            index = ip.index.replace("'", "")
            if index.startswith("ipv6"):
                try:
                    ipv6 = IPv6Address((index.replace("ipv6.0x", "")).decode("hex"))
                    self._ipv6_table[port_index].append(ipv6)
                except AddressValueError:
                    pass

            elif index.startswith("ipv4"):
                try:
                    ipv4 = IPv4Address((index.replace("ipv4.0x", "")).decode("hex"))
                    self._ipv4_table[port_index].append(ipv4)
                except AddressValueError:
                    pass

    def _convert_ipv6_table(self):
        for ipv6 in self._ipv6_snmp_table:
            if ipv6.index:
                # ToDo check how the index looks like
                #  and use spilt in case "." occurs only once.
                index_location = ipv6.index.find(".")
                port_index = ipv6.index[:index_location]
                ipv6_address = ipv6.index.replace(f"{port_index}.", "")
                if ipv6_address:
                    self._ipv6_table[port_index].append(ipv6_address)

    def set_port_attributes(self, port_object):
        port_object.ipv4_address = self.get_all_ipv4_by_index(
            port_object.relative_address.native_index
        )
        port_object.ipv6_address = self.get_all_ipv6_by_index(
            port_object.relative_address.native_index
        )

    def get_all_ipv4_by_index(self, port_index):
        [thread.join() for thread in self._thread_list]
        ip_addresses = self._ipv4_table.get(port_index)
        if ip_addresses:
            return ", ".join(ip_addresses)

    def get_all_ipv6_by_index(self, port_index):
        [thread.join() for thread in self._thread_list]
        ip_addresses = self._ipv6_table.get(port_index)
        if ip_addresses:
            return ", ".join(ip_addresses)
