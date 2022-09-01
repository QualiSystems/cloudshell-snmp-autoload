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
    ENTITY_VENDOR_TYPE,
)


class BaseEntity:
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
        result = self.entity_row_response.get(ENTITY_POSITION.object_name)
        return result.safe_value if result else ""

    @property
    def os_version(self):
        result = self.entity_row_response.get(ENTITY_OS_VERSION.object_name)
        return result.safe_value if result else ""

    @property
    def hw_version(self):
        result = self.entity_row_response.get(ENTITY_HW_VERSION.object_name)
        return result.safe_value if result else ""

    @property
    def description(self):
        result = self.entity_row_response.get(ENTITY_DESCRIPTION.object_name)
        return result.safe_value if result else ""

    @property
    def name(self):
        result = self.entity_row_response.get(ENTITY_NAME.object_name)
        return result.safe_value if result else ""

    @property
    def parent_id(self):
        result = self.entity_row_response.get(ENTITY_PARENT_ID.object_name)
        return result.safe_value if result else ""

    @property
    def entity_class(self):
        entity_class_response = self.entity_row_response.get(ENTITY_CLASS.object_name)
        return entity_class_response.safe_value if entity_class_response else ""

    @property
    def vendor_type(self):
        result = self.entity_row_response.get(ENTITY_VENDOR_TYPE.object_name)
        return result.safe_value if result else ""

    @property
    def model(self):
        result = self.entity_row_response.get(ENTITY_MODEL.object_name)
        return result.safe_value if result else ""

    @property
    def serial_number(self):
        result = self.entity_row_response.get(ENTITY_SERIAL.object_name)

        return result.safe_value if result else ""
