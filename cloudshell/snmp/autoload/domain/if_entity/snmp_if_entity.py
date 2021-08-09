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
    IF_TYPE_REPLACE_PATTERN = re.compile("^[/']|[/']$")
    PORT_IDS_PATTERN = re.compile(r"\d+(/\d+)*$", re.IGNORECASE)

    def __init__(self, port_index, port_row):
        self.if_index = port_index
        self._if_table_row = port_row
        self._if_alias = None
        self._if_name = None
        self._if_descr_name = None
        self._ips_list = None

    @property
    @lru_cache()
    def port_name(self):
        return self.if_name or self.if_descr_name

    @property
    @lru_cache()
    def if_name(self):
        return self._if_table_row.get(PORT_NAME.object_name).safe_value

    @property
    def if_descr_name(self):
        return self._if_table_row.get(PORT_DESCR_NAME.object_name).safe_value

    @property
    def if_port_description(self):
        return self._if_table_row.get(PORT_DESCRIPTION.object_name).safe_value

    @property
    def if_type(self):
        if_type = self._if_table_row.get(PORT_TYPE.object_name,).safe_value or "other"
        return if_type.strip("'")

    @property
    @lru_cache()
    def port_id(self):
        port_id = self.PORT_IDS_PATTERN.search(self.port_name)
        if port_id:
            return port_id.group()

    @property
    @lru_cache()
    def if_speed(self):
        return self._if_table_row.get(PORT_SPEED.object_name).safe_value

    @property
    @lru_cache()
    def if_mtu(self):
        return self._if_table_row.get(PORT_MTU.object_name).safe_value

    @property
    @lru_cache()
    def if_mac(self):
        return self._if_table_row.get(PORT_MAC.object_name).safe_value
