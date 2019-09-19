import re
from collections import OrderedDict

from cloudshell.snmp.autoload.core.snmp_oid_template import SnmpMibOidTemplate

ENTITY_VALID_CLASS_PATTERN = re.compile(
    r"stack|chassis|module|port|powerSupply|container|backplane"
)

ENTITY_POSITION = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalParentRelPos")
ENTITY_DESCRIPTION = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalDescr")
ENTITY_NAME = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalName")
ENTITY_PARENT_ID = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalContainedIn")
ENTITY_CLASS = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalClass")
ENTITY_VENDOR_TYPE = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalVendorType")
ENTITY_MODEL = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalModelName")
ENTITY_SERIAL = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalSerialNum")
ENTITY_OS_VERSION = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalSoftwareRev")
ENTITY_HW_VERSION = SnmpMibOidTemplate("ENTITY-MIB", "entPhysicalHardwareRev")
ENTITY_TO_IF_ID = SnmpMibOidTemplate("ENTITY-MIB", "entAliasMappingIdentifier")

ENTITY_VENDOR_TYPE_TO_CLASS_MAP = OrderedDict(
    [
        (re.compile(r"^\S+container"), "container"),
        (re.compile(r"^\S+chassis"), "chassis"),
        (re.compile(r"^\S+module"), "module"),
        (re.compile(r"^\S+port"), "port"),
        (re.compile(r"^\S+powersupply"), "powerSupply"),
    ]
)


ENTITY_TO_CONTAINER_PATTERN = re.compile(
    r"powershelf|^\S+sfp|^\S+xfr|^\S+xfp|"
    r"^\S+Container10GigBasePort|^\S+ModulePseAsicPlim"
)
