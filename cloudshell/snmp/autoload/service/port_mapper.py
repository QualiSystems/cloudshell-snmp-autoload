import re
import sys

from cloudshell.snmp.autoload.constants.entity_constants import ENTITY_TO_IF_ID

if sys.version_info >= (3, 0):
    from functools import lru_cache
else:
    from functools32 import lru_cache


class PortMappingService(object):
    PORT_EXCLUDE_RE = re.compile(
        r"stack|engine|management|mgmt|null|voice|foreign|"
        r"cpu|control\s*ethernet\s*port|console\s*port",
        re.IGNORECASE,
    )

    def __init__(self, snmp, if_table, logger):
        self._if_table = if_table
        self._snmp = snmp
        self._logger = logger

    @property
    @lru_cache()
    def port_mapping_table(self):
        port_map = {}
        for item in self._snmp.walk(ENTITY_TO_IF_ID):
            if item.safe_value:
                if_index = item.safe_value.replace("IF-MIB::ifIndex.", "")
                port = self._if_table.get_if_entity_by_index(if_index)
                if port:
                    index = item.index[: item.index.rfind(".")]
                    port_map[index] = port
                self._if_table.remove_port_from_unmapped_list(if_index)
        return port_map

    def get_mapping(self, port_entity):
        if_port = self.port_mapping_table.get(port_entity.base_entity.index)
        if not if_port:
            if_port = self._get_mapping(port_entity)
        return if_port

    def _get_mapping(self, port_entity):
        """Get mapping from entPhysicalTable to ifTable.

        Build mapping based on ent_alias_mapping_table if exists else build manually
        based on entPhysicalDescr <-> ifDescr mapping.

        :return: simple mapping from entPhysicalTable index to ifTable index:
        |        {entPhysicalTable index: ifTable index, ...}
        """
        port_if_entity = self._if_table.get_if_index_from_port_name(
            port_entity, self.PORT_EXCLUDE_RE
        )
        return port_if_entity
