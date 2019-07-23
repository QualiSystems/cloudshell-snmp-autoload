import re

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.domain.if_entity.snmp_if_port_channel_entity import SnmpIfPortChannel
from cloudshell.snmp.autoload.domain.if_entity.snmp_if_port_entity import SnmpIfPort
from cloudshell.snmp.autoload.domain.snmp_port_attr_tables import SnmpPortAttrTables


class SnmpIfTable(object):
    IF_PORT = SnmpIfPort
    IF_PORT_CHANNEL = SnmpIfPortChannel
    PORT_CHANNEL_NAME = ["port-channel", "bundle-ether"]
    PORT_EXCLUDE_LIST = ["mgmt", "management", "loopback", "null", "."]
    PORT_NAME_PATTERN = re.compile(r"((\d+/).+)")
    PORT_NAME_SECONDARY_PATTERN = re.compile(r"\d+")
    PORT_VALID_TYPE = re.compile(r"ethernet|other|propPointToPointSerial|fastEther|^otn", re.IGNORECASE)

    def __init__(self, snmp_handler, logger):
        self._snmp = snmp_handler
        self._logger = logger
        self._load_snmp_tables()
        self._if_entities_dict = dict()
        self._if_port_dict = dict()
        self._if_port_channels_dict = dict()
        self._port_exclude_list = self.PORT_EXCLUDE_LIST
        self.port_attributes_snmp_tables = SnmpPortAttrTables(snmp_handler, logger)

    def set_port_exclude_list(self, value):
        if value:
            self._port_exclude_list = value

    def set_port_attributes_service(self, value):
        self.port_attributes_snmp_tables = value

    @property
    def if_ports(self):
        if not self._if_port_dict:
            self._get_if_entities()
        return self._if_port_dict

    @property
    def if_port_channels(self):
        if not self._if_port_channels_dict:
            self._get_if_entities()
        return self._if_port_channels_dict

    def get_if_entity_by_index(self, if_index):
        if not self._if_entities_dict:
            self._get_if_entities()
        return self.if_ports.get(if_index) or self.if_port_channels.get(if_index)

    def _get_if_entities(self):
        for port in self._if_table:
            if any([exclude_port for exclude_port in self._port_exclude_list if
                    exclude_port in port.safe_value.lower()]):
                continue
            else:
                port_obj = self.IF_PORT(snmp_handler=self._snmp, logger=self._logger,
                                        port_name_response=port,
                                        port_attributes_snmp_tables=self.port_attributes_snmp_tables)
                self._if_port_dict[port.index] = port_obj

    def _get_port_channels(self):
        for port in self._if_table:
            if any([port_channel for port_channel in self.PORT_CHANNEL_NAME if port_channel in port.safe_value.lower()]):
                port_channel_obj = self.IF_PORT_CHANNEL(snmp_handler=self._snmp, logger=self._logger,
                                                        port_name_response=port,
                                                        port_attributes_snmp_tables=self.port_attributes_snmp_tables)
                self._if_port_channels_dict[port.index] = port_channel_obj

    def _load_snmp_tables(self):
        """ Load all cisco required snmp tables

        :return:
        """

        self._logger.info('Start loading MIB tables:')
        self._if_table = self._snmp.walk(port_constants.PORT_DESCR_NAME.get_snmp_mib_oid())
        if not self._if_table:
            self._if_table = self._snmp.walk(port_constants.PORT_NAME.get_snmp_mib_oid())
            if not self._if_table:
                self._if_table = self._snmp.walk(port_constants.PORT_INDEX.get_snmp_mib_oid())

        self._logger.info('ifIndex table loaded')

    def get_if_index_from_port_name(self, port_name, port_filter_pattern):
        if_table_re = None
        port_if_match = self.PORT_NAME_PATTERN.search(port_name)
        if not port_if_match:
            port_if_re = self.PORT_NAME_SECONDARY_PATTERN.findall(port_name)
            if port_if_re:
                if_table_re = "/".join(port_if_re)
        else:
            port_if_re = port_if_match.group()
            if_table_re = port_if_re
        if if_table_re:
            for interface_id in self.if_ports:
                interface = self.if_ports.get(interface_id)
                if interface and not self.PORT_VALID_TYPE.search(interface.if_type):
                    continue
                if port_filter_pattern.search(str(interface.if_name)):
                    continue
                if port_name == interface.if_name or port_name == interface.if_descr_name:
                    return interface
                port_pattern = re.compile(r"^\S*\D*{0}(/\D+|$)".format(if_table_re), re.IGNORECASE)
                if port_pattern.search(interface.if_name) \
                        or port_pattern.search(interface.if_descr_name):
                    return interface


# if __name__ == "__main__":
#     from cloudshell.core.logger.qs_logger import get_qs_logger
#     from cloudshell.snmp.snmp_parameters import SNMPV2Parameters
#     from cloudshell.snmp.cloudshell_snmp import Snmp
#
#     logger = get_qs_logger()
#     # ip = "192.168.105.8"
#     # ip = "192.168.73.66"
#     ip = "192.168.73.102"
#     # ip = "192.168.105.11"
#     # ip = "192.168.105.4"
#     # ip = "192.168.73.142"
#     # ip = "192.168.42.235"
#     comm = "public"
#     # comm = "private"
#     # comm = "Aa123456"
#     # comm = "Cisco"
#     snmp_params = SNMPV2Parameters(ip, comm)
#     logger.info("started")
#     snmp_handler = Snmp(logger=logger, snmp_parameters=snmp_params)
#
#     with snmp_handler.get_snmp_service() as snmp_service:
#         snmp_service.update_mib_file_sources("D:\\_Quali_Git\\cloudshell-networking-cisco\\cloudshell\\networking\\cisco\\mibs")
#         if_table = SnmpIfTable(logger=logger, snmp_handler=snmp_service)
#
#         for port_id, port in if_table.if_ports.iteritems():
#             print port.ipv4_address
#             print port.ipv6_address
#
#         print("done")

