from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock

from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel
from cloudshell.snmp.core.domain.quali_mib_table import QualiMibTable

from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable

from tests.cloudshell.snmp.autoload.data.physical_entities_data import (
    MOCK_SNMP_RESPONSE,
)


class TestPhysicalTable(TestCase):
    def setUp(self) -> None:
        self.table = self._prepare_env()

    def _prepare_env(self, data=None):
        if data is None:
            data = deepcopy(MOCK_SNMP_RESPONSE)
        logger = Mock()
        entity_table = self._create_entity_table(data, logger)
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
        return table

    def _create_entity_table(self, data, logger):
        snmp = Mock()
        response = QualiMibTable("test")
        response.update(data)
        snmp.get_multiple_columns.return_value = response

        return SnmpEntityTable(snmp, logger)

    def test_find_parent_containers(self):
        ent_index = "4116"
        position_id = "2"
        parent = self.table._find_parent_containers(ent_index)
        assert position_id == parent.position_id

    def test_find_chassis(self):
        ent_index = "20"
        position_id = "-1"
        parent = self.table.get_parent_chassis(ent_index)
        assert position_id == parent.position_id

    def test_find_parent_module(self):
        ent_index = "4117"
        position_id = "1"
        expected_id = "4015"

        parent = self.table.find_parent_module(ent_index)
        assert position_id == parent.position_id
        assert expected_id == parent.index

    def test_physical_structure_table(self):
        result = self.table.physical_structure_table
        assert result is not None
        assert len(self.table.physical_ports_list) == 6
        assert len(self.table.parent_dict) == 6
        assert all(self.table.parent_dict.get(x) for x in self.table.parent_dict)
        assert len(self.table._chassis_dict) == 1
        assert len(self.table._chassis_dict) == 1
        assert len(self.table.physical_chassis_dict) == 1
        assert len(self.table.physical_power_ports_dict) == 1

    def test_add_chassis_with_parent_chassis(self):
        response = deepcopy(MOCK_SNMP_RESPONSE)
        response["0"] = {
            "entPhysicalParentRelPos": Mock(safe_value="-1"),
            "entPhysicalDescr": Mock(
                safe_value="Cisco 2500 Series Wireless LAN Controller"
            ),
            "entPhysicalName": Mock(safe_value="Chassis"),
            "entPhysicalContainedIn": Mock(safe_value="4015"),
            "entPhysicalClass": Mock(safe_value=""),
            "entPhysicalVendorType": Mock(safe_value=""),
            "entPhysicalModelName": Mock(safe_value="AIR-CT2504-K9"),
            "entPhysicalSerialNum": Mock(safe_value="PSZ19201CDR"),
            "entPhysicalSoftwareRev": Mock(safe_value="8.2.100.0"),
            "entPhysicalHardwareRev": Mock(safe_value=""),
        }
        response["1"]["entPhysicalContainedIn"] = "0"
        table = self._prepare_env(response)

        result = table.physical_structure_table
        assert result is not None
