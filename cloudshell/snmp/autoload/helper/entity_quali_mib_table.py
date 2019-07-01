from cloudshell.snmp.autoload.constants.entity_constants import ENTITY_POSITION
from cloudshell.snmp.autoload.domain.entity.snmp_entity_base import BaseEntity


class EntityQualiMibTable(object):
    def __init__(self, snmp_service):
        self._snmp_service = snmp_service
        self._raw_entity_indexes = None
        self._raw_entity_position_table = None

    @property
    def raw_entity_indexes(self):
        if not self._raw_entity_indexes:
            self._raw_entity_indexes = list(self.raw_entity_position_table.keys())
        return self._raw_entity_indexes

    @property
    def raw_entity_position_table(self):
        if not self._raw_entity_position_table:
            self._raw_entity_position_table = self._snmp_service.get_table(ENTITY_POSITION.get_snmp_mib_oid())
        return self._raw_entity_position_table

    def get(self, k, d=None):
        result = self.raw_entity_position_table.get(k, {}).get(ENTITY_POSITION.mib_id, d)
        if result:
            result = BaseEntity(self._snmp_service, result)
        return result
