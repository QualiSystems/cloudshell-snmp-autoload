from functools import lru_cache

from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_PARENT_ID,
    ENTITY_TABLE_REQUIRED_COLUMNS,
)


class PhysicalStructure(object):
    def __init__(self, snmp_handler, logger):
        self._snmp_service = snmp_handler
        self._logger = logger

    @property
    @lru_cache()
    def physical_structure_snmp_table(self):
        return self._snmp_service.get_multiple_columns(ENTITY_TABLE_REQUIRED_COLUMNS)

    @property
    @lru_cache()
    def physical_structure_table(self):
        return self.physical_structure_snmp_table.filter_by_column(
            ENTITY_PARENT_ID.object_name
        )
