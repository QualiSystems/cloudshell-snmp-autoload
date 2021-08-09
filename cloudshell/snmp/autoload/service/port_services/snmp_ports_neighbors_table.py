import re
from collections import defaultdict
from logging import Logger
from threading import Thread

from cloudshell.snmp.core.snmp_service import SnmpService

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.service.port_services.port_service_interface import (
    PortAttributesServiceInterface,
)


class PortNeighbours(PortAttributesServiceInterface):
    ADJACENT_TEMPLATE = "{remote_host} through {remote_port}"
    LLDP_INDEX_PATTERN = re.compile(r".\d+.")
    LLDP_LOC_INTERFACE_NAME = "interfacename"
    LLDP_LOC_NETWORK_ADDR = "networkaddress"
    LLDP_LOC_MAC_ADDR = "macaddress"
    LLDP_LOC_INTERFACE_ALIAS = "interfacealias"

    def __init__(self, snmp_service: SnmpService, logger: Logger):
        self._snmp = snmp_service
        self._logger = logger
        self._adjacent_table = defaultdict(dict)
        self._used_adjacent_entries = []
        self._lldp_loc_snmp_table = {}
        self._lldp_rem_snmp_table = {}
        self._thread_list = []

    def load_snmp_tables(self):
        self._lldp_loc_snmp_table = self._snmp.get_multiple_columns(
            port_constants.PORT_LLDP_LOC_TABLE
        )
        self._lldp_rem_snmp_table = self._snmp.get_multiple_columns(
            port_constants.PORT_LLDP_REM_TABLE
        )
        if self._lldp_rem_snmp_table and self._lldp_loc_snmp_table:
            thread = Thread(target=self._convert_adjacent_table, name="LLDP converter")
            thread.start()
            self._thread_list.append(thread)

    def _convert_adjacent_table(self):
        lldp_rem_table = {}
        for lldp_rem_key, lldp_rem_data in self._lldp_rem_snmp_table.items():
            index_match = self.LLDP_INDEX_PATTERN.search(lldp_rem_key)
            if index_match:
                remote_sys_name = lldp_rem_data.get(
                    port_constants.PORT_ADJACENT_REM_NAME.object_name
                )
                remote_port_name = lldp_rem_data.get(
                    port_constants.PORT_ADJACENT_REM_PORT_DESCR.object_name
                )
                index = index_match.group().strip(".")
                lldp_rem_table[index] = self.ADJACENT_TEMPLATE.format(
                    remote_host=remote_sys_name, remote_port=remote_port_name,
                )
        if not lldp_rem_table:
            return
        for lldp_loc_id, lldp_loc_data in self._lldp_loc_snmp_table.items():
            if lldp_loc_id not in lldp_rem_table:
                continue
            loc_port_id = lldp_loc_data.get(
                port_constants.PORT_ADJACENT_LOC_ID.object_name
            )
            loc_port_desc = lldp_loc_data.get(
                port_constants.PORT_ADJACENT_LOC_DESC.object_name
            )
            loc_subtype = lldp_loc_data.get(
                port_constants.PORT_ADJACENT_LOC_SUBTYPE.object_name
            )
            loc_dict = {}
            adjacent_line = lldp_rem_table.get(lldp_loc_id)
            if adjacent_line:
                if loc_port_id:
                    loc_dict[loc_port_id.safe_value] = adjacent_line
                elif loc_port_desc:
                    loc_dict[loc_port_desc.safe_value] = adjacent_line
                subtype = loc_subtype.safe_value.lower().strip("'")
                self._adjacent_table[subtype].update(loc_dict)

    def set_port_attributes(self, port_object):
        port_object.adjacent = self.get_adjacent_by_port(port_object)

    def get_adjacent_by_port(self, port_object):
        """Get connected device interface and device name to the specified port id.

        Using cdp or lldp protocols
        :return: device's name and port connected to port id
        :rtype string
        """
        map(lambda thread: thread.join, self._thread_list)

        if self.LLDP_LOC_INTERFACE_NAME in self._adjacent_table:
            result = self._adjacent_table.get(self.LLDP_LOC_INTERFACE_NAME, {}).get(
                port_object.name
            )
            if result and result not in self._used_adjacent_entries:
                self._used_adjacent_entries.append(result)
                return result
        elif self.LLDP_LOC_NETWORK_ADDR in self._adjacent_table:
            if port_object.ipv4_address:
                result = self._adjacent_table.get(self.LLDP_LOC_NETWORK_ADDR, {}).get(
                    port_object.ipv4_address
                )
                if result and result not in self._used_adjacent_entries:
                    self._used_adjacent_entries.append(result)
                    return result
            if port_object.ipv6_address:
                result = self._adjacent_table.get(self.LLDP_LOC_NETWORK_ADDR, {}).get(
                    port_object.ipv6_address
                )
                if result and result not in self._used_adjacent_entries:
                    self._used_adjacent_entries.append(result)
                    return result
        elif self.LLDP_LOC_MAC_ADDR in self._adjacent_table:
            if port_object.mac_address:
                result = self._adjacent_table.get(self.LLDP_LOC_MAC_ADDR, {}).get(
                    port_object.mac_address
                )
                if result and result not in self._used_adjacent_entries:
                    self._used_adjacent_entries.append(result)
                    return result
        for lldp_data in self._adjacent_table.values():
            for lldp_rem_key, lldp_rem_data in lldp_data.items():
                if lldp_rem_data not in self._used_adjacent_entries and (
                    lldp_rem_key == port_object.port_description
                    or lldp_rem_key.startswith(port_object.port_description)
                ):
                    self._used_adjacent_entries.append(lldp_rem_data)
                    return lldp_rem_data
