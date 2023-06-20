from abc import ABC, abstractmethod

from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_VENDOR_TYPE_TO_CLASS_MAP,
)
from cloudshell.snmp.autoload.snmp.entities.snmp_entity_base import BaseEntity


class EntityHelperAbc(ABC):
    @abstractmethod
    def get_physical_class(self, entity: BaseEntity) -> str:
        raise NotImplementedError


class EntityHelper(EntityHelperAbc):
    ENTITY_SAFE_CLASS_LIST = ["port", "powersupply"]

    def get_physical_class(self, entity: BaseEntity) -> str:
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
                if key.search(entity.vendor_type_label):
                    entity_class = value

        return entity_class
