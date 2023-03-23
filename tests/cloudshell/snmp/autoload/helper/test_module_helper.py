from unittest import TestCase
from unittest.mock import Mock

from cloudshell.shell.standards.autoload_generic_models import GenericPort
from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel

from cloudshell.snmp.autoload.helper.module_helper import ModuleHelper
from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable


class TestPhysicalTable(TestCase):
    def test_get_parent_module_no_entity_no_entity_no_module_map(self):
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        entity_table = Mock()
        entity_table.physical_structure_snmp_table = {}
        table = PhysicalTable(entity_table, Mock(), resource_model)
        result = ModuleHelper(
            physical_table_service=table,
            resource_model=resource_model,
            logger=Mock(),
        ).get_parent_module("0-8")
        assert str(result.relative_address) == "CH0/M0/SM8"

    def test_get_parent_module_no_entity_no_entity_sub_module_map(self):
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        entity_table = Mock()
        entity_table.physical_structure_snmp_table = {}
        table = PhysicalTable(entity_table, Mock(), resource_model)
        helper = ModuleHelper(
            physical_table_service=table,
            resource_model=resource_model,
            logger=Mock(),
        )
        chassis = resource_model.entities.Chassis("0")
        module = resource_model.entities.Module("0")
        chassis.connect_module(module)
        sub_module = resource_model.entities.SubModule("8")
        module.connect_sub_module(sub_module)
        helper._sub_module_parents_map["0-0-8"] = sub_module
        result = helper.get_parent_module("0-8")
        assert str(result.relative_address) == "CH0/M0/SM8"
        assert result == sub_module

    def test_get_parent_module_no_entity_no_entity_module_map(self):
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        entity_table = Mock()
        entity_table.physical_structure_snmp_table = {}
        table = PhysicalTable(entity_table, Mock(), resource_model)
        helper = ModuleHelper(
            physical_table_service=table,
            resource_model=resource_model,
            logger=Mock(),
        )
        chassis = resource_model.entities.Chassis("0")
        module = resource_model.entities.Module("0")
        chassis.connect_module(module)
        helper._module_parents_map["0"] = module
        sub_module = resource_model.entities.SubModule("8")
        module.connect_sub_module(sub_module)
        result = helper.get_parent_module("0-8")
        assert str(result.relative_address) == "CH0/M0/SM8"

    def test_attach_port_to_parent_sub_module(self):
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        entity_table = Mock()
        entity_table.physical_structure_snmp_table = {}
        table = PhysicalTable(entity_table, Mock(), resource_model)
        module_helper = ModuleHelper(
            physical_table_service=table,
            resource_model=resource_model,
            logger=Mock(),
        )
        interface = GenericPort("4324")
        entity_port = GenericPort("4105")
        module_helper.attach_port_to_parent(
            entity_port=entity_port, if_port=interface, port_id="8-0"
        )
        assert str(interface.relative_address.parent_node) == "CH0/M8/SM0"
        assert str(interface.relative_address) == "CH0/M8/SM0/P4324"

    def test_attach_port_to_parent_module(self):
        resource_model = NetworkingResourceModel(
            "Resource Name", "Shell Name", "CS_Switch", Mock()
        )
        entity_table = Mock()
        entity_table.physical_structure_snmp_table = {}
        table = PhysicalTable(entity_table, Mock(), resource_model)
        module_helper = ModuleHelper(
            physical_table_service=table,
            resource_model=resource_model,
            logger=Mock(),
        )
        interface = GenericPort("4324")
        entity_port = GenericPort("4105")
        module_helper.attach_port_to_parent(
            entity_port=entity_port, if_port=interface, port_id="8"
        )
        assert str(interface.relative_address.parent_node) == "CH0/M8"
        assert str(interface.relative_address) == "CH0/M8/P4324"
