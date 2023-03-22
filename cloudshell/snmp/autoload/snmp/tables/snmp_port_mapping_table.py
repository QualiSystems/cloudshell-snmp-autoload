from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from cloudshell.snmp.autoload.constants.entity_constants import ENTITY_TO_IF_ID

if TYPE_CHECKING:
    LogicalId = str
    PhysId = str


class SnmpPortMappingTable:
    def __init__(self, snmp_handler, logger):
        self._snmp_service = snmp_handler
        self._logger = logger

    @property
    @lru_cache()
    def port_mapping_snmp_table(self) -> dict[LogicalId, PhysId]:
        """Port mapping logical to physical indices, based on
        ENTITY-MIB.entAliasMappingIdentifier."""  # noqa: D205, D400, D209
        port_map = {}
        for item in self._snmp_service.walk(ENTITY_TO_IF_ID):
            if item.safe_value:
                if_index = item.safe_value.replace("IF-MIB::ifIndex.", "")
                index = item.index[: item.index.rfind(".")]
                port_map[if_index] = index
        port_map = dict(sorted(port_map.items()))
        return port_map
