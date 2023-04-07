import re

from cloudshell.snmp.core.domain.snmp_oid import SnmpMibObject

SPECIAL_SYMBOLS = re.escape(".-|_[]")
CS_NOT_ALLOWED_STR_PATTERN = re.compile(rf"[^a-zA-Z\d\s{SPECIAL_SYMBOLS}]")

PORT_INDEX = SnmpMibObject("IF-MIB", "ifIndex")
PORT_DESCR_NAME = SnmpMibObject("IF-MIB", "ifDescr")
PORT_NAME = SnmpMibObject("IF-MIB", "ifName")
PORT_DESCRIPTION = SnmpMibObject("IF-MIB", "ifAlias")
PORT_TYPE = SnmpMibObject("IF-MIB", "ifType")
PORT_MTU = SnmpMibObject("IF-MIB", "ifMtu")
PORT_SPEED = SnmpMibObject("IF-MIB", "ifHighSpeed")
PORT_MAC = SnmpMibObject("IF-MIB", "ifPhysAddress")

PORT_DUPLEX_INDEX = SnmpMibObject("EtherLike-MIB", "dot3StatsIndex")
PORT_DUPLEX_DATA = SnmpMibObject("EtherLike-MIB", "dot3StatsDuplexStatus")

PORT_OLD_IP_INDEXES = SnmpMibObject("IP-MIB", "ipAdEntIfIndex")
PORT_MIXED_IP_INDEXES = SnmpMibObject("IP-MIB", "ipAddressIfIndex")
PORT_MIXED_IPV6_INDEXES = SnmpMibObject("IPV6-MIB", "ipv6AddrType")

PORT_CHANNEL_TABLE = SnmpMibObject("IEEE8023-LAG-MIB", "dot3adAggPortAttachedAggID")

PORT_ADJACENT_REM_NAME = SnmpMibObject("LLDP-MIB", "lldpRemSysName")
PORT_ADJACENT_REM_PORT_DESCR = SnmpMibObject("LLDP-MIB", "lldpRemPortDesc")
PORT_ADJACENT_LOC_DESC = SnmpMibObject("LLDP-MIB", "lldpLocPortDesc")
PORT_ADJACENT_LOC_ID = SnmpMibObject("LLDP-MIB", "lldpLocPortId")
PORT_ADJACENT_LOC_SUBTYPE = SnmpMibObject("LLDP-MIB", "lldpLocPortIdSubtype")

PORT_AUTO_NEG = SnmpMibObject("MAU-MIB", "ifMauAutoNegAdminStatus")

IF_TABLE = [
    PORT_INDEX,
    PORT_DESCR_NAME,
    PORT_NAME,
    PORT_DESCRIPTION,
    PORT_TYPE,
    PORT_MTU,
    PORT_SPEED,
    PORT_MAC,
]
PORT_DUPLEX_TABLE = [PORT_DUPLEX_INDEX, PORT_DUPLEX_DATA]
PORT_LLDP_LOC_TABLE = [
    PORT_ADJACENT_LOC_DESC,
    PORT_ADJACENT_LOC_SUBTYPE,
    PORT_ADJACENT_LOC_ID,
]
PORT_LLDP_REM_TABLE = [PORT_ADJACENT_REM_NAME, PORT_ADJACENT_REM_PORT_DESCR]
