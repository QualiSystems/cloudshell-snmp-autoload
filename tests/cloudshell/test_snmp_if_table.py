import unittest

from cloudshell.snmp.autoload.domain.if_entity.snmp_if_port_entity import SnmpIfPort
from cloudshell.snmp.autoload.snmp_if_table import SnmpIfTable


class TestSnmpIfTable(unittest.TestCase):
    def test_if_port(self):
        self.assertEqual(SnmpIfPort, SnmpIfTable.IF_PORT)
