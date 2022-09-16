from functools import lru_cache

from cloudshell.snmp.autoload.constants.entity_constants import ENTITY_TO_IF_ID


class SnmpPortMappingTable:
    def __init__(self, snmp_handler, logger):
        self._snmp_service = snmp_handler
        self._logger = logger

    @property
    @lru_cache()
    def port_mapping_snmp_table(self):
        port_map = {}
        for item in self._snmp_service.walk(ENTITY_TO_IF_ID):
            if item.safe_value:
                if_index = item.safe_value.replace("IF-MIB::ifIndex.", "")
                index = item.index[: item.index.rfind(".")]
                port_map[if_index] = index
        port_map = dict(sorted(port_map.items()))
        return port_map
