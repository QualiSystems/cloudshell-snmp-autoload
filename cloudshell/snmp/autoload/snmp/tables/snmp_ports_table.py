from functools import lru_cache

from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable

from cloudshell.snmp.autoload.constants import port_constants
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_associated_ports import (
    PortChannelsAssociatedPorts,
)
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_port_ip_tables import (
    PortIPTables,
)
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_ports_auto_negotioation import (
    PortAutoNegotiation,
)
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_ports_duplex_table import (
    PortDuplex,
)
from cloudshell.snmp.autoload.snmp.tables.port_attrs_snmp_tables.snmp_ports_neighbors_table import (
    PortNeighbours,
)


class SnmpPortsTable:
    def __init__(self, snmp_handler, logger):
        self._snmp = snmp_handler
        self._logger = logger
        self._port_ip_tables = PortIPTables(snmp_handler, logger)
        self._port_neighbors = PortNeighbours(snmp_handler, logger)
        self._port_auto_neg = PortAutoNegotiation(snmp_handler, logger)
        self._port_duplex = PortDuplex(snmp_handler, logger)
        self._port_channel_associated_ports = PortChannelsAssociatedPorts(
            snmp_handler, logger
        )

    @property
    @lru_cache()
    def port_table(self) -> QualiMibTable:
        """Load all cisco required snmp tables."""
        walk = self._snmp.get_multiple_columns(port_constants.IF_TABLE)
        return walk

    @property
    @lru_cache()
    def port_ip_table(self):
        """Load all cisco required snmp tables."""
        self._port_ip_tables.load_snmp_table()
        return self._port_ip_tables

    @property
    @lru_cache()
    def port_neighbors(self):
        """Load all cisco required snmp tables."""
        self._port_neighbors.load_snmp_table()
        return self._port_neighbors

    @property
    @lru_cache()
    def port_duplex(self):
        """Load all cisco required snmp tables."""
        self._port_duplex.load_snmp_table()
        return self._port_duplex

    @property
    @lru_cache()
    def port_auto_neg(self):
        """Load all cisco required snmp tables."""
        self._port_auto_neg.load_snmp_table()
        return self._port_auto_neg

    @property
    @lru_cache()
    def port_channel_associated_ports(self):
        """Load port channel members snmp tables."""
        self._port_channel_associated_ports.load_snmp_table()
        return self._port_channel_associated_ports

    def finalize_threads(self):
        self._port_ip_tables.finalize_thread()
        self._port_neighbors.finalize_thread()
        self._port_auto_neg.finalize_thread()
        self._port_duplex.finalize_thread()
        self._port_channel_associated_ports.finalize_thread()
