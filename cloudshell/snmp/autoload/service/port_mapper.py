import re


class PortMappingService(object):
    PORT_EXCLUDE_RE = re.compile(
        r"stack|engine|management|mgmt|null|voice|foreign|"
        r"cpu|control\s*ethernet\s*port|console\s*port",
        re.IGNORECASE,
    )

    def __init__(self, if_table, logger):
        self._if_table = if_table
        self._logger = logger

    def get_mapping(self, port_entity):
        if port_entity.alias_mapping:
            if_port = self._if_table.get_if_entity_by_index(port_entity.alias_mapping)
        else:
            if_port = self._get_mapping(port_entity.base_entity.name)
            if not if_port:
                if_port = self._get_mapping(port_entity.base_entity.description)
        return if_port

    def _get_mapping(self, port_descr):
        """Get mapping from entPhysicalTable to ifTable.

        Build mapping based on ent_alias_mapping_table if exists else build manually
        based on entPhysicalDescr <-> ifDescr mapping.

        :return: simple mapping from entPhysicalTable index to ifTable index:
        |        {entPhysicalTable index: ifTable index, ...}
        """
        port_if_entity = self._if_table.get_if_index_from_port_name(
            port_descr, self.PORT_EXCLUDE_RE
        )
        return port_if_entity
