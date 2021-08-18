from cloudshell.networking.arista.autoload.snmp_if_entity import SnmpIfEntity

from cloudshell.snmp.autoload.constants import port_constants


class PortSnmpHelper:
    def __init__(self, snmp_service, logger):
        self._snmp_service = snmp_service
        self._logger = logger
        self._if_port_dict = None
        self._if_port_channels_dict = None

    @property
    def ports_table(self):
        if not self._if_port_dict:
            self._get_if_entities()
        return self._if_port_dict

    @property
    def port_channels_table(self):
        if not self._if_port_channels_dict:
            self._get_if_entities()
        return self._if_port_channels_dict

    def get_if_entity_by_index(self, if_index):
        return self._if_port_dict.get(if_index) or self._if_port_channels_dict.get(
            if_index
        )

    def _get_if_entities(self):
        self._load_snmp_tables()
        for port_index, port_data in self._if_table.items():
            port: SnmpIfEntity = self._if_entity(port_index, port_data)
            if "." in port.port_name:
                continue
            if (
                not self.PORT_EXCLUDE_RE.search(port.if_name.lower())
                or not self.PORT_EXCLUDE_RE.search(port.if_descr_name.lower())
            ) and self.PORT_VALID_TYPE.search(port.if_type):
                self._add_port(port)
            else:
                pass
            if (
                self.PORT_CHANNEL_NAME
                and any(
                    port_channel
                    for port_channel in self.PORT_CHANNEL_NAME
                    if port_channel in port.port_name.lower()
                )
                or self.PORT_CHANNEL_VALID_TYPE.search(port.if_type)
            ):
                self._add_port_channel(port)

    def _add_port(self):
        pass

    def _load_snmp_tables(self):
        """Load all cisco required snmp tables."""
        self._logger.info("Start loading MIB tables:")

        self._if_table = self._snmp.get_multiple_columns(port_constants.IF_TABLE)

        self._port_ip_tables.load_snmp_tables()
        self._port_neighbors.load_snmp_tables()
        self._port_duplex.load_snmp_tables()
        self._port_auto_neg.load_snmp_tables()
        self._port_channel_associated_ports.load_snmp_tables()

        self._logger.info("ifIndex table loaded")
