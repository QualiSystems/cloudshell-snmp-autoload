import unittest
from unittest.mock import Mock

from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel

from cloudshell.snmp.autoload.services.port_table import PortsTable
from cloudshell.snmp.autoload.snmp.tables.snmp_ports_table import SnmpPortsTable

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
        resource_model = NetworkingResourceModel(
            "Resource Name",
            "Shell Name",
            "CS_Switch",
        )
        index = "527304960"
        port_value = PORT_SNMP_DATA.get(index)
        snmp.get_multiple_columns.return_value = PORT_SNMP_DATA
        if_table = PortsTable(
            resource_model=resource_model,
            ports_snmp_table=SnmpPortsTable(snmp, logger),
            logger=logger,
        )
        ports = if_table.ports_dict
        port_name = port_value["ifDescr"].safe_value.replace("/", "-")
        assert port_name == ports.get(index).name
