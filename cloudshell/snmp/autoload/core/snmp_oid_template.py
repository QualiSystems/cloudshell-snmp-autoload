from cloudshell.snmp.core.domain.snmp_oid import SnmpMibOid


class SnmpMibOidTemplate(object):
    def __init__(self, mib_name, mib_id):
        self.mib_name = mib_name
        self.mib_id = mib_id

    def get_snmp_mib_oid(self, index=None):
        return SnmpMibOid(self.mib_name, self.mib_id, index)
