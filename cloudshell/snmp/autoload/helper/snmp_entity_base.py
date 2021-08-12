from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_CLASS,
    ENTITY_DESCRIPTION,
    ENTITY_HW_VERSION,
    ENTITY_MODEL,
    ENTITY_NAME,
    ENTITY_OS_VERSION,
    ENTITY_PARENT_ID,
    ENTITY_POSITION,
    ENTITY_SERIAL,
    ENTITY_TO_CONTAINER_PATTERN,
    ENTITY_VENDOR_TYPE,
    ENTITY_VENDOR_TYPE_TO_CLASS_MAP,
)


class BaseEntity(object):
    def __init__(self, index, entity_row_response):
        self.index = index
        self.entity_row_response = entity_row_response
        self._parent_id = None
        self._entity_class = None
        self._vendor_type = None
        self._description = None
        self._name = None
        self._model = None
        self._serial_number = None

    @property
    def position_id(self):
        return self.entity_row_response.get(ENTITY_POSITION.object_name).safe_value

    @property
    def os_version(self):
        return self.entity_row_response.get(ENTITY_OS_VERSION.object_name).safe_value

    @property
    def hw_version(self):
        return self.entity_row_response.get(ENTITY_HW_VERSION.object_name).safe_value

    @property
    def description(self):
        return self.entity_row_response.get(ENTITY_DESCRIPTION.object_name).safe_value

    @property
    def name(self):
        return self.entity_row_response.get(ENTITY_NAME.object_name).safe_value

    @property
    def parent_id(self):
        return self.entity_row_response.get(ENTITY_PARENT_ID.object_name).safe_value

    @property
    def entity_class(self):
        if self._entity_class is None:
            self._entity_class = self._get_physical_class()
        return self._entity_class

    @property
    def vendor_type(self):
        return self.entity_row_response.get(ENTITY_VENDOR_TYPE.object_name).safe_value

    @property
    def model(self):
        return self.entity_row_response.get(ENTITY_MODEL.object_name).safe_value

    @property
    def serial_number(self):
        return self.entity_row_response.get(ENTITY_SERIAL.object_name).safe_value

    def _get_physical_class(self):
        if ENTITY_TO_CONTAINER_PATTERN.search(self.vendor_type):
            return "container"
        entity_class = self.entity_row_response.get(ENTITY_CLASS.object_name).safe_value

        if not entity_class or "other" in entity_class:
            if not self.vendor_type:
                return ""
            for key, value in ENTITY_VENDOR_TYPE_TO_CLASS_MAP.items():
                if key.search(self.vendor_type):
                    entity_class = value

        return entity_class
