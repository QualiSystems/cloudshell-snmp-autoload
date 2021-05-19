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
            self._raw_entity_indexes = self._snmp_service.walk(
                ENTITY_POSITION.get_snmp_mib_oid()
            )
        return self._raw_entity_indexes

    @property
    def raw_entity_position_table(self):
        if not self._raw_entity_position_table:
            self._raw_entity_position_table = self._snmp_service.table(
                ENTITY_POSITION.get_snmp_mib_oid()
            )
        return self._raw_entity_position_table

    def get(self, key_index):
        result = next(
            (key for key in self._raw_entity_indexes if key.index == str(key_index)),
            None,
        )
        if result:
            result = BaseEntity(self._snmp_service, result)
        return result
