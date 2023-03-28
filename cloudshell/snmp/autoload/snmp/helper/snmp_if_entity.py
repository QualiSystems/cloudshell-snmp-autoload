import re
from functools import lru_cache

from cloudshell.snmp.autoload.constants.port_constants import (
    PORT_DESCR_NAME,
    PORT_DESCRIPTION,
    PORT_MAC,
    PORT_MTU,
    PORT_NAME,
    PORT_SPEED,
    PORT_TYPE,
)


class SnmpIfEntity:
    PORT_IDS_PATTERN = re.compile(r"\d+(/\d+)*(\D\d+)*$", re.IGNORECASE)

    def __init__(self, port_index, port_row):
        self.if_index = port_index
        self._if_table_row = port_row

    @property
    @lru_cache()
    def port_name(self):
        result = self.if_name or self.if_descr_name
        return result.replace("/", "-").replace(":", "_")

    @property
    @lru_cache()
    def if_name(self):
        result = self._if_table_row.get(PORT_NAME.object_name)
        return result.safe_value if result else ""

    @property
    def if_descr_name(self):
        result = self._if_table_row.get(PORT_DESCR_NAME.object_name)
        return result.safe_value if result else ""

    @property
    def if_port_description(self):
        result = self._if_table_row.get(PORT_DESCRIPTION.object_name)
        if result:
            return result.safe_value

    @property
    def if_type(self):
        if_type = self._if_table_row.get(PORT_TYPE.object_name)
        result = "other"
        if if_type:
            result = if_type.safe_value.strip("'")
        return result

    @property
    @lru_cache()
    def port_id(self):
        port_id = self.PORT_IDS_PATTERN.search(self.port_name)
        if port_id:
            return port_id.group().replace("/", "-")

    @property
    @lru_cache()
    def if_speed(self):
        result = self._if_table_row.get(PORT_SPEED.object_name)
        return result.safe_value if result else ""

    @property
    @lru_cache()
    def if_mtu(self):
        result = self._if_table_row.get(PORT_MTU.object_name)
        if result:
            return result.safe_value

    @property
    @lru_cache()
    def if_mac(self):
        result = self._if_table_row.get(PORT_MAC.object_name)
        if result:
            return result.safe_value
