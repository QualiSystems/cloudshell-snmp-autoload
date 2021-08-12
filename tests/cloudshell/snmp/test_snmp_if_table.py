import unittest
from unittest.mock import Mock

from cloudshell.snmp.autoload.port_table import PortsTable

from tests.cloudshell.snmp.port_snmp_data import PORT_SNMP_DATA


class Port(Mock):
    def __init__(self, index, name, **kwargs):
        super().__init__("name", **kwargs)
        self.name = name
        self.relative_address = Mock()
        self.relative_address.native_index = index


class TestSnmpIfTable(unittest.TestCase):
    def test_if_ports_table(self):
        logger = Mock()
        snmp = Mock()
        resource_model = Mock()
        resource_model.entities.Port = Port
        index = "527304960"
        port_value = PORT_SNMP_DATA.get(index)
        snmp.get_multiple_columns.return_value = PORT_SNMP_DATA
        if_table = PortsTable(
            snmp_handler=snmp, logger=logger, resource_model=resource_model
        )
        if_table.load_snmp_tables()
        ports = if_table.if_ports
        port_name = port_value["ifDescr"].safe_value.replace("/", "-")
        assert port_name == ports.get(index).name
