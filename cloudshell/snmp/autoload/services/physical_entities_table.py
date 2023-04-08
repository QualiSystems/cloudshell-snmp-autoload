from __future__ import annotations

import re
from collections import defaultdict
from logging import Logger
from threading import Thread
from typing import TYPE_CHECKING

from cloudshell.snmp.autoload.exceptions.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.helper.entity_helper import EntityHelper
from cloudshell.snmp.autoload.helper.port_name_helper import convert_port_name
from cloudshell.snmp.autoload.snmp.entities.snmp_entity_base import BaseEntity
from cloudshell.snmp.autoload.snmp.tables.snmp_entity_table import SnmpEntityTable

if TYPE_CHECKING:
    PhysId = str


class PhysicalTable:
    MODULE_EXCLUDE_LIST = ["fan", "cpu"]
    MODULE_TO_CONTAINER_LIST = []

    def __init__(
        self,
        entity_table: SnmpEntityTable,
        logger: Logger,
        resource_model,
    ):
        """Init PhysicalTable.

        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        """
        self.entity_table = entity_table
        self._logger = logger
        self._resource_model = resource_model
        self._physical_structure_table = {}
        self._module_exclude_pattern = None
        self.power_port_exclude_pattern = None
        self.chassis_exclude_pattern = None
        self._port_list = []
        self._power_port_dict = {}
        self._chassis_dict = {}
        self.parent_dict = {}
        self.port_parent_dict = {}
        self._modules_hierarchy_dict = defaultdict(list)
        self.chassis_ids_dict = {}
        self.chassis_helper = EntityHelper()
        self._snmp_physical_structure_table = (
            self.entity_table.physical_structure_snmp_table
        )
        self._thread = Thread(
            name=self.__class__.__name__, target=self._get_entity_table
        )
        self._thread.start()

    @property
    def module_exclude_pattern(self):
        pattern = "|".join(self.MODULE_EXCLUDE_LIST)
        return re.compile(pattern, re.IGNORECASE)

    @property
    def physical_ports_list(self):
        self._thread.join()
        return self._port_list

    @property
    def physical_power_ports_dict(self):
        """Power ports dict based on Entity-MIB.

        :rtype: dict[PhysId,
        cloudshell.shell.standards.autoload_generic_models.AbstractResource]
        """
        self._thread.join()
        return self._power_port_dict

    @property
    def physical_chassis_dict(self):
        """Chassis dict based on Entity-MIB.

        :rtype: dict[PhysId, cloudshell.shell.standards.autoload_generic_models.AbstractResource]
        """
        self._thread.join()
        if not self._chassis_dict:
            self._add_dummy_chassis("0")
        return self._chassis_dict

    @property
    def physical_structure_table(self):
        """Entities table based on Entity-MIB.

        :rtype: dict[PhysId,
        cloudshell.shell.standards.autoload_generic_models.AbstractResource]
        """
        self._thread.join()
        return self._physical_structure_table

    def _get_entity_table(self):
        """Read Entity-MIB and filter out device's structure and all it's elements.

        Like ports, modules, chassis, etc.
        :rtype: QualiMibTable
        :return: structured and filtered EntityPhysical table.
        """
        for entity_index in self._snmp_physical_structure_table:
            if entity_index in self._physical_structure_table:
                continue
            self._add_entity(entity_index)

    def load_entity(self, entity_index) -> BaseEntity:
        entity_data = self.entity_table.physical_structure_snmp_table.get(entity_index)
        return BaseEntity(entity_index, entity_data)

    def _add_entity(self, entity_index):
        if entity_index not in self.entity_table.physical_structure_table:
            return
        entity = self.load_entity(entity_index)
        entity_class = self.chassis_helper.get_physical_class(entity)
        if "port" in entity_class:
            self._add_port(entity)
        elif "powersupply" in entity_class.lower():
            self._add_power_port(entity)
        elif "chassis" in entity_class.lower():
            self._add_chassis(entity)

    def _add_chassis(self, entity):
        index = "0" if entity.position_id == "-1" else entity.position_id
        chassis_object = self._resource_model.entities.Chassis(index=index)

        chassis_object.model = entity.model
        chassis_object.serial_number = entity.serial_number
        duplicate_chassis = next(
            (
                obj
                for obj in self._chassis_dict.values()
                if obj.serial_number == chassis_object.serial_number
                and obj.model == chassis_object.model
            ),
            None,
        )
        if duplicate_chassis:
            return

        self._logger.debug(f"Discovered a Chassis: {entity.model}")
        self._chassis_dict[entity.index] = chassis_object
        self._physical_structure_table[entity.index] = chassis_object
        self.chassis_ids_dict[index] = chassis_object

    def _add_port(self, entity):
        name = self._pick_port_name(entity)
        if not name:
            return

        port_object = self._resource_model.entities.Port(index=entity.index, name=name)
        parent_module = self.find_parent_module(entity.index)

        port_object.port_description = entity.description
        self._logger.debug(f"Discovered a Port: {entity.model}")
        self._physical_structure_table[entity.index] = port_object
        self._port_list.append(entity.index)
        if not parent_module:
            return
        self.parent_dict[port_object] = parent_module.index

    def _pick_port_name(self, entity):
        port_name = "Port"
        name_is_unique = True
        descr_is_unique = True
        ent_name = convert_port_name(entity.name)
        ent_desc = convert_port_name(entity.description)
        for k in self.entity_table.physical_structure_snmp_table:
            if k == entity.index:
                continue
            v_entity = self.load_entity(k)
            if v_entity.entity_class == entity.entity_class:
                if convert_port_name(v_entity.name) == ent_name:
                    name_is_unique = False
                if convert_port_name(v_entity.description) == ent_desc:
                    descr_is_unique = False
            if not descr_is_unique and not name_is_unique:
                break
        if name_is_unique:
            port_name = ent_name
        elif descr_is_unique:
            port_name = ent_desc
        return port_name

    def _add_power_port(self, entity):
        power_port_object = self._resource_model.entities.PowerPort(
            index=entity.position_id
        )
        power_port_object.model = entity.model
        power_port_object.port_description = entity.description
        power_port_object.version = entity.hw_version
        power_port_object.serial_number = entity.serial_number
        self._logger.debug(f"Discovered a Power Port: {entity.model}")
        self._power_port_dict[entity.index] = power_port_object

    def _find_parent_containers(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        parent = self.load_entity(parent_index)
        if not parent.entity_row_response:
            return
        entity_class = self.chassis_helper.get_physical_class(parent)
        if entity_class in ["container", "backplane"]:
            return parent
        elif (
            self.module_exclude_pattern.search(parent.vendor_type)
            or "port" in entity_class
        ):
            return self._find_parent_containers(parent_index)

    def find_parent_module(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        if not parent_index:
            return
        parent = self.load_entity(parent_index)
        if not parent.entity_row_response:
            return
        entity_class = self.chassis_helper.get_physical_class(parent)
        if "module" in entity_class and not self.module_exclude_pattern.search(
            parent.vendor_type
        ):
            return parent
        if "chassis" in entity_class:
            return parent
        else:
            return self.find_parent_module(parent_index)

    def create_module(self, entity_index: str):
        entity = self.load_entity(entity_index)
        if not entity.entity_row_response:
            return
        if self.module_exclude_pattern and self.module_exclude_pattern.search(
            entity.vendor_type
        ):
            return

        position_id = entity.position_id
        parent_container = self._find_parent_containers(entity.index)
        parent_module_index = entity.parent_id
        if parent_container:
            position_id = parent_container.position_id
            parent_module_index = self.entity_table.physical_structure_table.get(
                parent_container.index
            )

        module_object = self._resource_model.entities.Module(index=position_id)
        module_object.model = entity.model
        module_object.version = entity.os_version
        module_object.serial_number = entity.serial_number
        self._physical_structure_table[entity.index] = module_object
        self._logger.debug(f"Discovered a Module: {entity.model}")
        self.parent_dict[module_object] = parent_module_index
        return module_object

    def get_parent_chassis(self, entity_id):
        parent_index = self.entity_table.physical_structure_table.get(entity_id)
        if not parent_index:
            raise GeneralAutoloadError("Error loading parent entity")
        parent = self.load_entity(parent_index)
        entity_class = self.chassis_helper.get_physical_class(parent)
        if "chassis" in entity_class:
            return parent
        else:
            return self.get_parent_chassis(parent_index)

    def _add_dummy_chassis(self, chassis_id):
        """Create Dummy Chassis."""
        chassis_object = self._resource_model.entities.Chassis(index=chassis_id)

        self._chassis_dict[chassis_id] = chassis_object
        self._physical_structure_table[chassis_id] = chassis_object
        self.chassis_ids_dict[chassis_id] = chassis_object
        self._logger.warning(f"Added Dummy Chassis with index {chassis_id}")
