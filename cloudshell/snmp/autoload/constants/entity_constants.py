import re

from cloudshell.snmp.core.domain.snmp_oid import SnmpMibObject

ENTITY_VALID_CLASS_PATTERN = re.compile(
    r"stack|chassis|module|port|powerSupply|container|backplane"
)

CONTAINER_MATCH_PATTERN = re.compile(r"^\S+container", re.IGNORECASE)
CHASSIS_MATCH_PATTERN = re.compile(r"^\S+chassis", re.IGNORECASE)
MODULE_MATCH_PATTERN = re.compile(r"^\S+module", re.IGNORECASE)
PORT_MATCH_PATTERN = re.compile(r"^\S+port", re.IGNORECASE)
POWER_SUPPLY_MATCH_PATTERN = re.compile(r"^\S+powersupply", re.IGNORECASE)

ENTITY_VENDOR_TYPE_TO_CLASS_MAP = {
    CONTAINER_MATCH_PATTERN: "container",
    CHASSIS_MATCH_PATTERN: "chassis",
    MODULE_MATCH_PATTERN: "module",
    PORT_MATCH_PATTERN: "port",
    POWER_SUPPLY_MATCH_PATTERN: "powerSupply",
}

ENTITY_POSITION = SnmpMibObject("ENTITY-MIB", "entPhysicalParentRelPos")
ENTITY_DESCRIPTION = SnmpMibObject("ENTITY-MIB", "entPhysicalDescr")
ENTITY_NAME = SnmpMibObject("ENTITY-MIB", "entPhysicalName")
ENTITY_PARENT_ID = SnmpMibObject("ENTITY-MIB", "entPhysicalContainedIn")
ENTITY_CLASS = SnmpMibObject("ENTITY-MIB", "entPhysicalClass")
ENTITY_VENDOR_TYPE = SnmpMibObject("ENTITY-MIB", "entPhysicalVendorType")
ENTITY_MODEL = SnmpMibObject("ENTITY-MIB", "entPhysicalModelName")
ENTITY_SERIAL = SnmpMibObject("ENTITY-MIB", "entPhysicalSerialNum")
ENTITY_OS_VERSION = SnmpMibObject("ENTITY-MIB", "entPhysicalSoftwareRev")
ENTITY_HW_VERSION = SnmpMibObject("ENTITY-MIB", "entPhysicalHardwareRev")
ENTITY_TO_IF_ID = SnmpMibObject("ENTITY-MIB", "entAliasMappingIdentifier")

ENTITY_TABLE_REQUIRED_COLUMNS = [
    ENTITY_POSITION,
    ENTITY_DESCRIPTION,
    ENTITY_NAME,
    ENTITY_PARENT_ID,
    ENTITY_CLASS,
    ENTITY_VENDOR_TYPE,
    ENTITY_MODEL,
    ENTITY_SERIAL,
    ENTITY_OS_VERSION,
    ENTITY_HW_VERSION,
]
