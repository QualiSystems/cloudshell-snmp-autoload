from unittest.mock import Mock

import pytest

from cloudshell.shell.standards.networking.autoload_model import NetworkingResourceModel

from cloudshell.snmp.autoload.services.port_table import PortsTable
from cloudshell.snmp.autoload.snmp.tables.snmp_ports_table import SnmpPortsTable

from tests.cloudshell.snmp.port_snmp_data import PORT_SNMP_DATA

API = Mock(
    DecryptPassword=lambda x: Mock(Value=x),
    GetResourceDetails=lambda x: Mock(UniqueIdentifier="uniq id", ChildResources=[]),
)


@pytest.mark.parametrize(
    "resource_model",
    [NetworkingResourceModel("Resource Name", "Shell Name", "CS_Switch", API)],
)
def test_if_ports_table(resource_model):
    logger = Mock()
    snmp = Mock()
    resource_model._api.GetResourceDetails = Mock(
        UniqueIdentifier="uniq id", ChildResources=[]
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
