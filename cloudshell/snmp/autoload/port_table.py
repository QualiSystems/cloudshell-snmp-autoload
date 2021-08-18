import re

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.helper.snmp_if_entity import SnmpIfEntity
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_associated_ports import (
    PortChannelsAssociatedPorts,
)
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_port_ip_tables import (
    PortIPTables,
)
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_ports_auto_negotioation import (  # noqa #E501
    PortAutoNegotiation,
)
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_ports_duplex_table import (
    PortDuplex,
)
from cloudshell.snmp.autoload.snmp_tables.port_attributes_snmp_tables.snmp_ports_neighbors_table import (  # noqa #E501
    PortNeighbours,
)


class PortsTable(object):
    ALLOWED_PORT_MODEL_NAME = ["GenericPort"]
    ALLOWED_PORT_CHANNEL_MODEL_NAME = ["GenericPortChannel"]
    PORT_CHANNEL_NAME = ["ae", "port-channel", "bundle-ether"]
    # ToDo clean Port Channel name list before release
    PORT_CHANNEL_VALID_TYPE = re.compile(r"ieee8023adLag", re.IGNORECASE,)
    PORT_VALID_TYPE = re.compile(
        r"ethernet|other|propPointToPointSerial|fastEther|opticalChannel|^otn",
        re.IGNORECASE,
    )
    PORT_EXCLUDE_RE = re.compile(
        r"stack|engine|management|mgmt|null|voice|foreign|"
        r"cpu|control\s*ethernet\s*port|console\s*port",
        re.IGNORECASE,
    )

    def __init__(self, snmp_handler, logger, resource_model, is_port_id_unique=False):
        self._snmp = snmp_handler
        self._logger = logger
        self._resource_model = resource_model
        self._if_table = {}
        self._if_entity = SnmpIfEntity
        self._port_ip_tables = PortIPTables(snmp_handler, logger)
        self._port_neighbors = PortNeighbours(snmp_handler, logger)
        self._port_auto_neg = PortAutoNegotiation(snmp_handler, logger)
        self._port_duplex = PortDuplex(snmp_handler, logger)
        self._port_channel_associated_ports = PortChannelsAssociatedPorts(
            snmp_handler, logger
        )
        self._duplex_table = {}
        self._adjacent_table = {}
        self._auto_negotiation = {}
        self._if_port_dict = {}
        self._if_port_channels_dict = {}
        self.port_name_to_object_map = {}
        self._unmapped_ports_list = []
        self._is_port_id_unique = is_port_id_unique

    @property
    def if_ports(self):
        # ToDo Add a brief description of returned structure.
        """{index: port object} dict.

        :return:
        """
        if not self._if_port_dict:
            self._get_if_entities()
        return self._if_port_dict

    @property
    def if_port_channels(self):
        # ToDo Add a brief description of returned structure.
        if not self._if_port_channels_dict:
            self._get_if_entities()
        return self._if_port_channels_dict

    def _add_port(self, port: SnmpIfEntity):
        port_object = self._resource_model.entities.Port(
            index=port.if_index, name=port.port_name.replace("/", "-")
        )
        port_object.mac_address = port.if_mac
        port_object.l2_protocol_type = port.if_type.replace("'", "")
        port_object.ipv4_address = self._port_ip_tables.get_all_ipv4_by_index(
            port.if_index
        )
        port_object.ipv6_address = self._port_ip_tables.get_all_ipv6_by_index(
            port.if_index
        )
        port_object.port_description = port.if_port_description
        port_object.bandwidth = port.if_speed
        port_object.mtu = port.if_mtu
        port_object.duplex = self._port_duplex.get_duplex_by_port_index(port.if_index)
        self._port_auto_neg.set_port_attributes(port_object)
        port_object.adjacent = self._port_neighbors.get_adjacent_by_port(port_object)

        self._if_port_dict[port.if_index] = port_object
        if port.if_name:
            self.port_name_to_object_map[port.if_name.lower()] = port.if_index
        if port.if_descr_name:
            self.port_name_to_object_map[port.if_descr_name.lower()] = port.if_index

    def _add_port_channel(self, port: SnmpIfEntity):
        port_channel_object = self._resource_model.entities.PortChannel(
            index=port.if_index
        )

        associated_port_list = self._port_channel_associated_ports.set_port_attributes(
            port.if_index
        )
        if associated_port_list:
            port_channel_object.associated_ports = ", ".join(
                [x.name for x in map(self.get_if_entity_by_index, associated_port_list)]
            )
        port_channel_object.port_description = port.if_port_description
        port_channel_object.ipv4_address = self._port_ip_tables.get_all_ipv4_by_index(
            port.if_index
        )
        port_channel_object.ipv6_address = self._port_ip_tables.get_all_ipv6_by_index(
            port.if_index
        )
        self._if_port_channels_dict[port.if_index] = port_channel_object

    def load_snmp_tables(self):
        """Load all cisco required snmp tables."""
        self._logger.info("Start loading MIB tables:")

        self._if_table = self._snmp.get_multiple_columns(port_constants.IF_TABLE)

        self._port_ip_tables.load_snmp_tables()
        self._port_neighbors.load_snmp_tables()
        self._port_duplex.load_snmp_tables()
        self._port_auto_neg.load_snmp_tables()
        self._port_channel_associated_ports.load_snmp_tables()

        self._logger.info("ifIndex table loaded")
