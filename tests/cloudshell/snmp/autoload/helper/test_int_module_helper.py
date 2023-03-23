from unittest import TestCase
from unittest.mock import Mock

from cloudshell.shell.standards.autoload_generic_models import GenericPort
from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel
from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable

from cloudshell.snmp.autoload.helper.module_helper import ModuleHelper
from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable

from tests.cloudshell.snmp.autoload.data.physical_entities_data import (
    MOCK_SNMP_RESPONSE,
)


class TestPhysicalTable(TestCase):
    def setUp(self) -> None:
        self._logger = Mock()
        entity_table = self._create_entity_table()
        self._resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        self.table = PhysicalTable(entity_table, self._logger, self._resource_model)
        self.table.MODULE_EXCLUDE_LIST = [
            r"powershelf|cevsfp|cevxfr|cevSensor|cevCpuTypeCPU|"
            r"cevxfp|cevContainer10GigBasePort|cevModuleDIMM|"
            r"cevModulePseAsicPlim|cevModule\S+Storage$|"
            r"cevModuleFabricTypeAsic|cevModuleCommonCardsPSEASIC|"
            r"cevFan|cevCpu|cevSensor|cevContainerDaughterCard"
        ]

    def _create_module_helper(self):
        return ModuleHelper(
            physical_table_service=self.table,
            resource_model=self._resource_model,
            logger=self._logger,
        )

    def _create_entity_table(self):
        snmp = Mock()
        response = QualiMibTable("test")
        response.update(MOCK_SNMP_RESPONSE)
        snmp.get_multiple_columns.return_value = response

        return SnmpEntityTable(snmp, self._logger)

    def test_get_parent_entity_by_ids_known_1_module(self):
        result = self._create_module_helper().get_parent_module("0-8")
        assert str(result.relative_address) == "CH0/M0/SM8"

    def test_get_parent_entity_by_ids_known_2_modules(self):
        module_helper = self._create_module_helper()
        result = module_helper.get_parent_module("0-8-1")
        assert str(result.relative_address) == "CH0/M8/SM1"

    def test_get_parent_entity_by_ids_unknown_2_modules(self):
        result = self._create_module_helper().get_parent_module("0-9-1")
        assert str(result.relative_address) == "CH0/M9/SM1"

    def test_get_parent_entity_by_ids_known_1_module_no_chassis(self):
        result = self._create_module_helper().get_parent_module("8")
        assert str(result.relative_address) == "CH0/M8"

    def test_get_parent_entity_by_ids_unknown_2_modules_no_chassis(self):
        result = self._create_module_helper().get_parent_module("9-1")
        assert str(result.relative_address) == "CH0/M9/SM1"

    def test_attach_port_to_parent(self):
        _ = self.table.physical_structure_table
        module_helper = self._create_module_helper()
        interface = GenericPort("4324")
        entity_port = GenericPort("4105")
        module_helper.attach_port_to_parent(
            entity_port=entity_port, if_port=interface, port_id="8-0"
        )
        assert str(interface.relative_address.parent_node) == "CH0/M8/SM0"
        assert str(interface.relative_address) == "CH0/M8/SM0/P4324"
