from functools import lru_cache

from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_PARENT_ID,
    ENTITY_TABLE_REQUIRED_COLUMNS,
    ENTITY_TO_IF_ID,
)


class SnmpEntityTable:
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
        table = self.physical_structure_snmp_table.get_columns(
            ENTITY_PARENT_ID.object_name
        )
        return {
            k: v.get(ENTITY_PARENT_ID.object_name).safe_value
            for k, v in table.items()
            if v.get(ENTITY_PARENT_ID.object_name)
            and v.get(ENTITY_PARENT_ID.object_name).safe_value is not None
        }

    @property
    @lru_cache()
    def port_mapping_snmp_table(self):
        port_map = {}
        for item in self._snmp_service.walk(ENTITY_TO_IF_ID):
            if item.safe_value:
                if_index = item.safe_value.replace("IF-MIB::ifIndex.", "")
                index = item.index[: item.index.rfind(".")]
                port_map[if_index] = index

        return port_map
