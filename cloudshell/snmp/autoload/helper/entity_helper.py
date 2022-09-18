from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_TO_CONTAINER_PATTERN,
    ENTITY_VENDOR_TYPE_TO_CLASS_MAP,
)
from cloudshell.snmp.autoload.snmp.helper.snmp_entity_base import BaseEntity


class EntityHelper:
    def get_physical_class(self, entity: BaseEntity):
        if ENTITY_TO_CONTAINER_PATTERN.search(entity.vendor_type):
            return "container"
        entity_class = entity.entity_class
        if not entity_class or "other" in entity_class:
            if not entity.vendor_type:
                if entity.position_id == "-1" and (
                    "chassis" in entity.name.lower()
                    or "chassis" in entity.description.lower()
                ):
                    return "chassis"
                return ""
            for key, value in ENTITY_VENDOR_TYPE_TO_CLASS_MAP.items():
                if key.search(entity.vendor_type):
                    entity_class = value

        return entity_class