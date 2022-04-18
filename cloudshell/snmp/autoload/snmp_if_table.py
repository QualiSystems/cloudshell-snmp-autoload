import re

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.domain.if_entity.snmp_if_port_channel_entity import (
    SnmpIfPortChannel,
)
from cloudshell.snmp.autoload.domain.if_entity.snmp_if_port_entity import SnmpIfPort
from cloudshell.snmp.autoload.domain.snmp_port_attr_tables import SnmpPortAttrTables


class SnmpIfTable(object):
    IF_PORT = SnmpIfPort
    IF_PORT_CHANNEL = SnmpIfPortChannel
    PORT_CHANNEL_NAME = ["port-channel", "bundle-ether"]  # ToDo remove it from here
    PORT_EXCLUDE_LIST = ["mgmt", "management", "loopback", "null", "."]

    PORT_VALID_TYPE = re.compile(
        r"ethernet|other|propPointToPointSerial|fastEther|opticalChannel|^otn",
        re.IGNORECASE,
    )

    def __init__(self, snmp_handler, logger, is_port_id_unique=False):
        self._snmp = snmp_handler
        self._logger = logger
        self._load_snmp_tables()
        self.if_port_type = self.IF_PORT
        self.if_port_channel_type = self.IF_PORT_CHANNEL
        self._if_entities_dict = {}
        self._if_port_dict = {}
        self._if_port_channels_dict = {}
        self.port_exclude_list = self.PORT_EXCLUDE_LIST
        self.port_attributes_service = SnmpPortAttrTables(snmp_handler, logger)
        self._port_name_to_object_map = {}
        self._unmapped_ports_list = []
        self._is_port_id_unique = is_port_id_unique

    @property
    def if_ports(self):
        if not self._if_port_dict:
            self._get_if_entities()
        return self._if_port_dict

    @property
    def _unmapped_ports(self):
        if not self._unmapped_ports_list:
            self._get_if_entities()
        return self._unmapped_ports_list

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
            if "." in port.safe_value:
                continue
            if any(
                port_channel
                for port_channel in self.PORT_CHANNEL_NAME
                if port_channel in port.safe_value.lower()
            ):
                self._add_port_channel(port)
            elif not any(
                exclude_port
                for exclude_port in self.port_exclude_list
                if exclude_port in port.safe_value.lower()
            ):
                self._add_port(port)

    def _add_port(self, port):
        port_obj = self.if_port_type(
            snmp_handler=self._snmp,
            logger=self._logger,
            port_name_response=port,
            port_attributes_snmp_tables=self.port_attributes_service,
        )
        self._if_port_dict[port.index] = port_obj
        if port_obj.if_descr_name:
            self._port_name_to_object_map[port_obj.if_descr_name.lower()] = port_obj
        if port_obj.if_name:
            self._port_name_to_object_map[port_obj.if_name.lower()] = port_obj
        self._unmapped_ports_list.append(port.index)

    def _add_port_channel(self, port):
        port_channel_obj = self.if_port_channel_type(
            snmp_handler=self._snmp,
            logger=self._logger,
            port_name_response=port,
            port_attributes_snmp_tables=self.port_attributes_service,
        )
        self._if_port_channels_dict[port.index] = port_channel_obj

    def _load_snmp_tables(self):
        """Load all cisco required snmp tables."""
        self._logger.info("Start loading MIB tables:")
        self._if_table = self._snmp.walk(
            port_constants.PORT_DESCR_NAME.get_snmp_mib_oid()
        )
        if not self._if_table:
            self._if_table = self._snmp.walk(
                port_constants.PORT_NAME.get_snmp_mib_oid()
            )
            if not self._if_table:
                self._if_table = self._snmp.walk(
                    port_constants.PORT_INDEX.get_snmp_mib_oid()
                )

        self._logger.info("ifIndex table loaded")

    def get_if_index_from_port_name(self, port, port_filter_pattern):
        interface = self._get_by_port_name(port.base_entity.name.lower())
        if not interface:
            interface = self._get_by_port_name(port.base_entity.description.lower())
        if interface and interface.if_index in self._unmapped_ports:
            self.remove_port_from_unmapped_list(interface.if_index)
            return interface
        for interface_id in self._unmapped_ports:
            interface = self.if_ports.get(interface_id)
            if interface and not self.PORT_VALID_TYPE.search(interface.if_type):
                continue
            if port_filter_pattern.search(str(interface.if_name)):
                continue
            if (
                port.port_name_pattern
                and port.port_name_pattern.search(interface.if_name)
            ) or (
                port.port_desc_pattern
                and port.port_desc_pattern.search(interface.if_descr_name)
            ):
                self._unmapped_ports.remove(interface_id)
                return interface
            if (
                port.port_name_id_pattern
                and port.port_name_id_pattern.search(interface.if_name)
            ) or (
                port.port_desc_id_pattern
                and port.port_desc_id_pattern.search(interface.if_descr_name)
            ):
                self._unmapped_ports.remove(interface_id)
                return interface
            if (
                interface.port_id == port.port_name_id
                or interface.port_id == port.port_desc_id
            ):
                self._unmapped_ports.remove(interface_id)
                return interface

    def remove_port_from_unmapped_list(self, interface_id):
        if interface_id in self._unmapped_ports:
            self._unmapped_ports.remove(interface_id)

    def _get_by_port_name(self, name):
        return self._port_name_to_object_map.get(name)
