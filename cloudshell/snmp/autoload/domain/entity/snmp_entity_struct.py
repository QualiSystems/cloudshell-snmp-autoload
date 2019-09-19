import re

from cloudshell.snmp.autoload.constants.entity_constants import (
    ENTITY_HW_VERSION,
    ENTITY_OS_VERSION,
    ENTITY_TO_IF_ID,
)


class BaseModuleEntity(object):
    def __init__(self, base_entity):
        """

        :type base_entity: cloudshell.snmp.autoload.domain.entity.snmp_entity_base.BaseEntity
        """
        self.base_entity = base_entity
        self._position_id = base_entity.position_id

    @property
    def parent_id(self):
        return self.base_entity.parent_id

    @property
    def position_id(self):
        return self._position_id

    @position_id.setter
    def position_id(self, id):
        self._position_id = id

    @property
    def index(self):
        return self.base_entity.index

    @property
    def serial_number(self):
        return self.base_entity.serial_number

    @property
    def model(self):
        return self.base_entity.model


class Chassis(BaseModuleEntity):
    pass


class Module(BaseModuleEntity):
    def __init__(self, base_entity):
        super(Module, self).__init__(base_entity)
        self._os_version = None

    @property
    def os_version(self):
        if self._os_version is None:
            self._os_version = self.base_entity.snmp_service.get_property(
                ENTITY_OS_VERSION.get_snmp_mib_oid(self.base_entity.index)
            ).safe_value
        return self._os_version


class PowerPort(BaseModuleEntity):
    def __init__(self, base_entity):
        super(PowerPort, self).__init__(base_entity)
        self._hw_version = None

    @property
    def hw_version(self):
        if self._hw_version is None:
            self._hw_version = self.base_entity.snmp_service.get_property(
                ENTITY_HW_VERSION.get_snmp_mib_oid(self.base_entity.index)
            ).safe_value
        return self._hw_version


class Port(BaseModuleEntity):
    def __init__(self, base_entity):
        super(Port, self).__init__(base_entity)
        self._alias_mapping = None

    @property
    def alias_mapping(self):
        if not self._alias_mapping:
            alias_mapping_list = self.base_entity.snmp_service.get_next(
                ENTITY_TO_IF_ID.get_snmp_mib_oid(self.base_entity.index)
            )
            if alias_mapping_list:
                for alias_mapping in alias_mapping_list:
                    if (
                        alias_mapping.mib_id == ENTITY_TO_IF_ID.mib_id
                        and alias_mapping.index.startswith("{}.".format(self.index))
                    ):
                        self._alias_mapping = alias_mapping.safe_value.replace(
                            "IF-MIB::ifIndex.", ""
                        )
                        break
        return self._alias_mapping
