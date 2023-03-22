from unittest import TestCase
from unittest.mock import Mock

from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel
from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable

from cloudshell.snmp.autoload.helper.port_helper import PortHelper
from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.services.port_table import PortsTable
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable

from tests.cloudshell.snmp.autoload.data.physical_entities_data import (
    MOCK_SNMP_RESPONSE,
)


class TestPortHelper(TestCase):
    PORT_ID = "3-14"

    def _create_entity_table(self, logger):
        snmp = Mock()
        response = QualiMibTable("test")
        response.update(MOCK_SNMP_RESPONSE)
        snmp.get_multiple_columns.return_value = response

        return SnmpEntityTable(snmp, logger)

    def _create_port_helper(
        self,
        port_id=PORT_ID,
    ):
        logger = Mock()
        entity_table = self._create_entity_table(logger)
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        table = PhysicalTable(entity_table, logger, resource_model)
        table.MODULE_EXCLUDE_LIST = [
            r"powershelf|cevsfp|cevxfr|cevSensor|cevCpuTypeCPU|"
            r"cevxfp|cevContainer10GigBasePort|cevModuleDIMM|"
            r"cevModulePseAsicPlim|cevModule\S+Storage$|"
            r"cevModuleFabricTypeAsic|cevModuleCommonCardsPSEASIC|"
            r"cevFan|cevCpu|cevSensor|cevContainerDaughterCard"
        ]
        port_table = PortsTable(resource_model, Mock(), logger)
        port_entity = Mock()
        port_entity.return_value.port_id = port_id
        port_table._if_entity = port_entity
        return PortHelper(
            physical_table_service=table,
            port_table_service=port_table,
            port_mapping_table_service=Mock(),
            resource_model=resource_model,
            logger=logger,
        )

    def test_is_not_valid_mgmt_port(self):
        interface = Mock()
        interface.name = "mgmt"
        interface.description = "GigabitEthernet0/0"
        port_helper = self._create_port_helper()

        result = port_helper._is_valid_port(interface)
        assert result is False

    def test_is_not_valid_mgmt_port_descr(self):
        interface = Mock()
        interface.description = "mgmt"
        interface.name = "GigabitEthernet0/0"
        port_helper = self._create_port_helper()

        result = port_helper._is_valid_port(interface)
        assert result is False

    def test_is_valid_port(self):
        interface = Mock()
        interface.name = "Gi0/0"
        interface.description = "GigabitEthernet0/0"
        port_helper = self._create_port_helper()

        result = port_helper._is_valid_port(interface)
        assert result
