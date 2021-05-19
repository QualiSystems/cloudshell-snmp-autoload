from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_CLASS,
    ENTITY_DESCRIPTION,
    ENTITY_MODEL,
    ENTITY_NAME,
    ENTITY_PARENT_ID,
    ENTITY_SERIAL,
    ENTITY_TO_CONTAINER_PATTERN,
    ENTITY_VENDOR_TYPE,
    ENTITY_VENDOR_TYPE_TO_CLASS_MAP,
)


class BaseEntity(object):
    def __init__(self, snmp_service, snmp_position_response):
        self.snmp_service = snmp_service
        self.index = snmp_position_response.index
        self._position_id = snmp_position_response.safe_value
        self._parent_id = None
        self._entity_class = None
        self._vendor_type = None
        self._description = None
        self._name = None
        self._model = None
        self._serial_number = None

    @property
    def position_id(self):
        if self._position_id == "-1":
            self._position_id = "0"
        return self._position_id

    @property
    def description(self):
        if self._description is None:
            self._description = self.snmp_service.get_property(
                ENTITY_DESCRIPTION.get_snmp_mib_oid(self.index)
            )
        return self._description.safe_value

    @property
    def name(self):
        if self._name is None:
            self._name = self.snmp_service.get_property(
                ENTITY_NAME.get_snmp_mib_oid(self.index)
            )
        return self._name.safe_value or ""

    @property
    def parent_id(self):
        if self._parent_id is None:
            self._parent_id = self.snmp_service.get_property(
                ENTITY_PARENT_ID.get_snmp_mib_oid(self.index)
            ).safe_value
        return self._parent_id

    @property
    def entity_class(self):
        if self._entity_class is None:
            self._entity_class = self._get_physical_class()
        return self._entity_class

    @property
    def vendor_type(self):
        if self._vendor_type is None:
            self._vendor_type = self.snmp_service.get_property(
                ENTITY_VENDOR_TYPE.get_snmp_mib_oid(self.index)
            )
            if self._vendor_type:
                self._vendor_type = self._vendor_type.safe_value
        return self._vendor_type

    @property
    def model(self):
        if self._model is None:
            self._model = (
                self.snmp_service.get_property(
                    ENTITY_MODEL.get_snmp_mib_oid(self.index)
                )
                or self.name
            )
        return self._model.safe_value

    @property
    def serial_number(self):
        if self._serial_number is None:
            self._serial_number = (
                self.snmp_service.get_property(
                    ENTITY_SERIAL.get_snmp_mib_oid(self.index)
                ).safe_value
                or ""
            )
        return self._serial_number

    def _get_physical_class(self):
        if ENTITY_TO_CONTAINER_PATTERN.search(self.vendor_type):
            return "container"
        entity_class = self.snmp_service.get_property(
            ENTITY_CLASS.get_snmp_mib_oid(self.index)
        ).safe_value.strip("'")

        if not entity_class or "other" in entity_class:
            if not self.vendor_type:
                return ""
            for key, value in ENTITY_VENDOR_TYPE_TO_CLASS_MAP.items():
                if key.search(self.vendor_type):
                    # ToDo could be a potential issue here.
                    entity_class = value

        return entity_class
