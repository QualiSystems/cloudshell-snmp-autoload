from cloudshell.snmp.core.domain.snmp_oid import SnmpMibObject


class SnmpMibOidTemplate(object):
    def __init__(self, mib_name, mib_id):
        self.mib_name = mib_name
        self.mib_id = mib_id

    def get_snmp_mib_oid(self, index=None):
        return SnmpMibObject(self.mib_name, self.mib_id, index)
