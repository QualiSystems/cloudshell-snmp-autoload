import re
from functools import lru_cache
from logging import Logger
from typing import Dict

from cloudshell.snmp.autoload.helper.port_name_helper import convert_port_name
from cloudshell.snmp.autoload.snmp.entities.snmp_if_entity import SnmpIfEntity
from cloudshell.snmp.autoload.snmp.tables.snmp_ports_table import SnmpPortsTable


class PortsTable:
    ALLOWED_PORT_MODEL_NAME = ["GenericPort"]
    ALLOWED_PORT_CHANNEL_MODEL_NAME = ["GenericPortChannel"]
    PORT_CHANNEL_NAME_LIST = [
        r"^ae\d+",
        r"^port-channel\d+",
        r"^bundle-ether\d+",
        r"lag",
    ]
    PORT_NAME_LIST = []
    PORT_CHANNEL_VALID_TYPE_LIST = [r"ieee8023adLag", r"propVirtual", r"other"]
    PORT_VALID_TYPE_LIST = [
        r"ethernet|other|propPointToPointSerial",
        r"fastEther|opticalChannel|^otn",
    ]
    PORT_EXCLUDE_LIST = [
        r"stack|engine|management|mgmt|null|voice",
        r"control\s*ethernet\s*port|console\s*port",
    ]
    PORT_CHANNEL_EXCLUDE_LIST = []

    def __init__(
        self,
        resource_model,
        ports_snmp_table: SnmpPortsTable,
        logger: Logger,
    ):
        """Init.

        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        """
        self._resource_model = resource_model
        self._if_table = {}
        self._if_entity = SnmpIfEntity
        self._duplex_table = {}
        self._adjacent_table = {}
        self._auto_negotiation = {}
        self._if_port_dict = {}
        self._if_port_channels_dict = {}
        self.port_name_to_object_map = {}
        self._unmapped_ports_list = []
        self.ports_tables = ports_snmp_table
        self._logger = logger

    @property
    @lru_cache()
    def port_exclude_re(self):
        port_exclude = "|".join(self.PORT_EXCLUDE_LIST)
        return re.compile(port_exclude, re.IGNORECASE)

    @property
    @lru_cache()
    def port_channel_name_re(self):
        port_channel_name = "|".join(self.PORT_CHANNEL_NAME_LIST)
        return re.compile(port_channel_name, re.IGNORECASE)

    @property
    @lru_cache()
    def port_name_re(self):
        port_name = "|".join(self.PORT_NAME_LIST)
        return re.compile(port_name, re.IGNORECASE)

    @property
    @lru_cache()
    def port_channel_exclude_re(self):
        port_channel_exclude = "|".join(self.PORT_CHANNEL_EXCLUDE_LIST)
        return re.compile(port_channel_exclude, re.IGNORECASE)

    @property
    @lru_cache()
    def port_valid_type_re(self):
        port_valid = "|".join(self.PORT_VALID_TYPE_LIST)
        return re.compile(port_valid, re.IGNORECASE)

    @property
    @lru_cache()
    def port_channel_valid_type_re(self):
        port_channel_valid = "|".join(self.PORT_CHANNEL_VALID_TYPE_LIST)
        return re.compile(port_channel_valid, re.IGNORECASE)

    @property
    def ports_dict(self):
        """Port index to Port object map.

        Port object is the one defined in the standard's resource_model.
        Usually, ifIndex is used by various vendors as a mapping key, between
        interface table and other tables. Including Physical structure table.
        :rtype: dict[str, cloudshell.shell.standards.autoload_generic_models.GenericPort]  # noqa: E501
        """
        if not self._if_port_dict:
            self._get_if_entities()
            self._if_port_dict = dict(sorted(self._if_port_dict.items()))
        return self._if_port_dict

    @property
    def port_channels_dict(self) -> Dict[str, object]:
        """Port index to Port Channel object map.

        Port Channel object is the one defined in the standard's resource_model.
        Usually, ifIndex is used by various vendors as a mapping key, between
        interface table and other tables.
        """
        if not self._if_port_channels_dict:
            self._get_if_entities()
        return self._if_port_channels_dict

    def _get_if_entities(self):
        for port_index in self.ports_tables.port_table:
            port: SnmpIfEntity = self.load_if_port(port_index)
            if self._is_valid_port_channel(port):
                self._add_port_channel(port)
                continue

            if self._is_valid_port(port):
                self._add_port(port)

    def _is_valid_port(self, port: SnmpIfEntity):
        if self.PORT_VALID_TYPE_LIST:
            if not self.port_valid_type_re.search(port.if_type):
                return False
        if self.PORT_EXCLUDE_LIST:
            if port.if_name and self.is_wrong_port(port.if_name):
                return False
            if port.if_descr_name and self.is_wrong_port(port.if_descr_name):
                return False
        if self.PORT_NAME_LIST:
            if self.port_name_re.search(port.if_name):
                return False
            if self.port_name_re.search(port.if_descr_name):
                return False
        return True

    def _is_valid_port_channel(self, port: SnmpIfEntity):
        if self.PORT_CHANNEL_EXCLUDE_LIST:
            if port.if_name and self.is_wrong_port_channel(port.if_name):
                return False
            if port.if_descr_name and self.is_wrong_port_channel(port.if_descr_name):
                return False
        if self.PORT_CHANNEL_VALID_TYPE_LIST:
            if not self.port_channel_valid_type_re.search(port.if_type):
                return False
        if self.PORT_CHANNEL_NAME_LIST:
            if not self.port_channel_name_re.search(
                port.if_name
            ) and not self.port_channel_name_re.search(port.if_descr_name):
                return False
        return True

    def _add_port(self, port: SnmpIfEntity):
        port_object = self._resource_model.entities.Port(
            index=port.if_index, name=convert_port_name(port.port_name)
        )
        port_object.mac_address = port.if_mac
        port_object.l2_protocol_type = port.if_type.replace("'", "")
        port_object.ipv4_address = (
            self.ports_tables.port_ip_table.get_all_ipv4_by_index(port.if_index)
        )
        port_object.ipv6_address = (
            self.ports_tables.port_ip_table.get_all_ipv6_by_index(port.if_index)
        )
        port_object.port_description = port.if_port_description
        port_object.bandwidth = port.if_speed
        port_object.mtu = port.if_mtu
        port_object.duplex = self.ports_tables.port_duplex.get_duplex_by_port_index(
            port.if_index
        )
        port_object.auto_negotiation = (
            self.ports_tables.port_auto_neg.get_value_by_index(port.if_index)
        )
        port_object.adjacent = self.ports_tables.port_neighbors.get_adjacent_by_port(
            port_object, port
        )

        self._if_port_dict[port.if_index] = port_object

    def load_if_port(self, index: str) -> SnmpIfEntity:
        port_data = self.ports_tables.port_table.get(index)
        return self._if_entity(index, port_data)

    def _add_port_channel(self, port: SnmpIfEntity):
        port_channel_object = self._resource_model.entities.PortChannel(
            index=port.port_id, name=convert_port_name(port.port_name)
        )
        associated_port_list = (
            self.ports_tables.port_channel_associated_ports.get_associated_ports(
                port.if_index
            )
        )
        if associated_port_list:
            port_channel_object.associated_ports = ", ".join(
                [self._get_if_name_by_index(x) for x in associated_port_list]
            )
        port_channel_object.port_description = port.if_port_description
        port_channel_object.ipv4_address = (
            self.ports_tables.port_ip_table.get_all_ipv4_by_index(port.if_index)
        )
        port_channel_object.ipv6_address = (
            self.ports_tables.port_ip_table.get_all_ipv6_by_index(port.if_index)
        )
        self._if_port_channels_dict[port.if_index] = port_channel_object

    def _get_if_name_by_index(self, if_index):
        if if_index in self._if_port_dict:
            return self._if_port_dict.get(if_index).name
        snmp_port_data = self.load_if_port(if_index)
        return snmp_port_data.port_name

    def is_wrong_port(self, port_name):
        return self.port_exclude_re.search(port_name.lower())

    def is_wrong_port_channel(self, port_name):
        return self.port_channel_exclude_re.search(port_name.lower())
