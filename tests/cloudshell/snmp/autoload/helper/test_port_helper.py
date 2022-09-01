from unittest import TestCase
from unittest.mock import Mock

from cloudshell.shell.standards.autoload_generic_models import GenericPort
from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel
from cloudshell.snmp.autoload.helper.port_helper import PortHelper
from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable
from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable

from tests.cloudshell.snmp.autoload.data.physical_entities_data import (
    MOCK_SNMP_RESPONSE,
)


class TestPortHelper(TestCase):
    PORT_ID = "3-14"

    def setUp(self) -> None:
        logger = Mock()
        entity_table = self._create_entity_table(logger)
        resource_model = NetworkingResourceModel(
            "Resource Name",
            "Shell Name",
            "CS_Switch",
        )
        table = PhysicalTable(entity_table, logger, resource_model)
        table.MODULE_EXCLUDE_LIST = [
            r"powershelf|cevsfp|cevxfr|cevSensor|cevCpuTypeCPU|"
            r"cevxfp|cevContainer10GigBasePort|cevModuleDIMM|"
            r"cevModulePseAsicPlim|cevModule\S+Storage$|"
            r"cevModuleFabricTypeAsic|cevModuleCommonCardsPSEASIC|"
            r"cevFan|cevCpu|cevSensor|cevContainerDaughterCard"
        ]
        port_table = Mock()
        port_table.load_if_port.return_value.port_id = self.PORT_ID
        self.port_helper = PortHelper(
            physical_table_service=table,
            port_table_service=port_table,
            port_mapping_table_service=Mock(),
            resource_model=resource_model,
            logger=logger,
        )

    def _create_entity_table(self, logger):
        snmp = Mock()
        response = QualiMibTable("test")
        response.update(MOCK_SNMP_RESPONSE)
        snmp.get_multiple_columns.return_value = response

        return SnmpEntityTable(snmp, logger)

    def _create_port_helper(self, port_id=PORT_ID):
        logger = Mock()
        entity_table = self._create_entity_table(logger)
        resource_model = NetworkingResourceModel(
            "Resource Name",
            "Shell Name",
            "CS_Switch",
        )
        table = PhysicalTable(entity_table, logger, resource_model)
        table.MODULE_EXCLUDE_LIST = [
            r"powershelf|cevsfp|cevxfr|cevSensor|cevCpuTypeCPU|"
            r"cevxfp|cevContainer10GigBasePort|cevModuleDIMM|"
            r"cevModulePseAsicPlim|cevModule\S+Storage$|"
            r"cevModuleFabricTypeAsic|cevModuleCommonCardsPSEASIC|"
            r"cevFan|cevCpu|cevSensor|cevContainerDaughterCard"
        ]
        port_table = Mock()
        port_table.load_if_port.return_value.port_id = port_id
        return PortHelper(
            physical_table_service=table,
            port_table_service=port_table,
            port_mapping_table_service=Mock(),
            resource_model=resource_model,
            logger=logger,
        )

    def test_guess_port_parent_unknown_one_module(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper()

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M3"

    def test_guess_port_parent_unknown_two_modules(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper("3-2-12")

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M3/SM2"

    def test_guess_port_parent_known_one_module(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper("0-7-12")

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M7"

    def test_guess_port_parent_known_two_modules(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper("0-8-1-12")

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M8/SM1"

    def test_guess_port_parent_known_one_module_no_chassis_id(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper("7-12")

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M7"

    def test_guess_port_parent_known_two_modules_no_chassis_id(self):
        interface = GenericPort("4324")
        if_index = Mock()
        port_helper = self._create_port_helper("8-1-12")

        port_helper._guess_port_parent(if_index, interface)
        assert str(interface.relative_address.parent_node) == "CH0/M8/SM1"
