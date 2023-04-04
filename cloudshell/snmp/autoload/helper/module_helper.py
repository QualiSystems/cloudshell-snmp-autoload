import re

from cloudshell.snmp.autoload.exceptions.snmp_autoload_error import GeneralAutoloadError


class ModuleHelper:
    def __init__(self, resource_model, physical_table_service, logger):
        self._resource_model = resource_model
        self._physical_table_service = physical_table_service
        self._logger = logger
        self.port_id_to_module_map = {}
        self._module_parents_map = {}
        self._sub_module_parents_map = {}
        self.modules_list = []

    def get_parent_module(self, port_id, entity=None):
        chassis = list(self._physical_table_service.physical_chassis_dict.values())[0]
        if not port_id and not entity:
            return chassis
        module_generated = False
        port_ids = self._get_port_parent_ids_list(port_id)
        parent = None
        if entity:
            parent = self.get_entity_parent_entity(entity)
        if not parent:
            parent = self.generate_module(port_ids.pop(-1))
            module_generated = True
        elif parent and port_ids:
            parent.relative_address.native_index = port_ids.pop(-1)
        if parent and parent.name.lower().startswith("chassis"):
            return parent
        parent_id = "-".join(port_ids)
        module_parent = None
        if port_ids:
            module_parent = self._module_parents_map.get(parent_id)
            if module_parent:
                parent = self._convert_module_to_sub_module(parent)
                parent = self._attach_entity_to_parent(module_parent, parent)
                self._update_port_to_module_map(port_id, parent)
                return parent
        if not module_parent:
            module_parent = self.get_entity_parent_entity(parent)
            if (
                module_parent
                and not parent_id
                and not module_parent.name.lower().startswith("chassis")
            ):
                parent_id = module_parent.relative_address.native_index
                _module_parent = self._module_parents_map.get(parent_id)
                if _module_parent:
                    parent = self._convert_module_to_sub_module(parent)
                    parent = self._attach_entity_to_parent(_module_parent, parent)
                    self._update_port_to_module_map(port_id, parent)
                    return parent
        if not module_parent and parent_id:
            module_parent = self.generate_module(parent_id)

        if module_parent:
            if module_parent.name.lower().startswith("chassis"):
                chassis = module_parent
                if not port_id:
                    module_ids = "-".join(self._get_modules_ids(chassis, module=parent))
                    parent_module = self._module_parents_map.get(module_ids)
                    if not parent_module:
                        parent_module = next(
                            (
                                x
                                for x in self.port_id_to_module_map.values()
                                if self.find_module_ids(x) == module_ids
                            ),
                            None,
                        )
                        if parent_module:
                            return parent_module
                if len(port_ids) > 0 and module_generated:
                    parent_module = self.generate_module(parent_id)
                    _ = self._attach_entity_to_parent(parent_module, parent)
                elif len(port_ids) > 0:
                    index = port_ids.pop(-1)
                    parent.relative_address.native_index = index
                    self._update_port_to_module_map(parent_id, parent)
                parent = self._attach_entity_to_parent(chassis, parent)
                self.port_id_to_module_map[port_id] = parent
                return parent
            else:
                if parent_id:
                    module_parent.relative_address.native_index = parent_id[
                        parent_id.rfind("-") + 1 :
                    ]

                parent = self._convert_module_to_sub_module(parent)
        else:
            self._logger.warning(f"No module parent found for port {port_id}")

        return self._update_structure(
            entity=entity,
            chassis=chassis,
            port_id=port_id,
            parent_id=parent_id,
            module_parent=module_parent,
            parent=parent,
        )

    def _update_structure(
        self, entity, chassis, port_id, parent_id, module_parent=None, parent=None
    ):
        if len(self._physical_table_service.physical_chassis_dict.items()) > 1:
            detected_chassis = self.get_entity_parent_entity(entity)
            while detected_chassis and not detected_chassis.name.lower().startswith(
                "chassis"
            ):
                self._update_module_attrs(detected_chassis, module_parent)
                self._update_module_attrs(module_parent, parent)
                detected_chassis = self.get_entity_parent_entity(detected_chassis)

            if detected_chassis:
                chassis = detected_chassis
        parent_ids = "-".join(self._get_modules_ids(chassis, module_parent, parent))
        if chassis and module_parent and parent:
            new_parent = self._sub_module_parents_map.get(parent_ids)
            if new_parent:
                return new_parent
        if module_parent:
            new_module_parent = None
            if len(parent_id.split("-")) == 2 and not parent_ids.startswith(parent_id):
                new_module_parent = self._module_parents_map.get(
                    parent_ids[: parent_ids.rfind("-")]
                )
            if not new_module_parent:
                module_parent = self._attach_entity_to_parent(chassis, module_parent)
            else:
                module_parent = new_module_parent
        elif parent:
            parent = self._attach_entity_to_parent(chassis, parent)
        else:
            return chassis
        if len(parent_id.split("-")) == 2 and parent_id != parent_ids:
            new_parent = self.port_id_to_module_map.get(parent_ids)
            if new_parent:
                return new_parent
        if not parent.relative_address.parent_node and module_parent:
            parent = self._attach_entity_to_parent(module_parent, parent)
        if port_id not in self.port_id_to_module_map:
            self._update_port_to_module_map(port_id, parent)

        if module_parent and parent_id not in self._module_parents_map:
            self._update_module_map(parent_id, module_parent)
        return parent

    def _get_modules_ids(self, chassis=None, module_parent=None, module=None):
        modules_ids = []
        if chassis:
            modules_ids.append(chassis.relative_address.native_index)
        if module_parent:
            modules_ids.append(module_parent.relative_address.native_index)
        if module:
            modules_ids.append(module.relative_address.native_index)
        return modules_ids

    def _update_port_to_module_map(self, port_parent_id, parent):
        if (
            port_parent_id not in self.port_id_to_module_map
            and not parent.name.lower().startswith("chassis")
        ):
            parent_id_list = port_parent_id.split("-")
            rel_address = self.find_module_ids(parent)
            self._sub_module_parents_map[rel_address] = parent
            if not parent.name.lower().startswith("sub"):
                self._update_module_map(port_parent_id, parent)
            elif parent.name.lower().startswith("sub") and len(parent_id_list) > 1:
                self.port_id_to_module_map[port_parent_id] = parent

            if len(parent_id_list) > 1 and rel_address != port_parent_id:
                self.port_id_to_module_map[rel_address] = parent

    def _update_module_map(self, port_parent_id, parent):
        if (
            port_parent_id not in self._module_parents_map
            and not parent.name.lower().startswith("chassis")
        ):
            rel_address = self.find_module_ids(parent)
            self._module_parents_map[port_parent_id] = parent
            self._module_parents_map[rel_address] = parent

    def find_module_ids(self, module):
        module_ids = []
        rel_address_match = re.findall(r"\d+", str(module.relative_address))
        if rel_address_match:
            module_ids = rel_address_match
        return "-".join(module_ids)

    def _convert_module_to_sub_module(self, module):
        if module:
            if module.name.lower().startswith("sub"):
                return module
            sub_module = self.generate_sub_module(module.relative_address.native_index)
            self._update_module_attrs(module, sub_module)
            return sub_module

    def _update_module_attrs(self, source_module, target_module):
        if source_module and target_module:
            target_module.model = source_module.model
            if hasattr(target_module, "version"):
                target_module.version = source_module.version
            target_module.serial_number = source_module.serial_number
            target_module.model_name = source_module.model_name

    def _attach_entity_to_parent(self, parent, entity):
        """Attach entity to parent if not already attached.

        Parent stands for chassis or module
        Entity stands for module or sub-module
        """
        if parent and entity and entity not in parent.extract_sub_resources():
            new_entity = next(
                (
                    x
                    for x in parent.extract_sub_resources()
                    if self._has_same_module_id(x, entity.relative_address.native_index)
                ),
                None,
            )
            if new_entity:
                entity = new_entity
            else:
                if isinstance(entity, self._resource_model.entities.SubModule):
                    parent.connect_sub_module(entity)
                elif isinstance(entity, self._resource_model.entities.Module):
                    parent.connect_module(entity)
                else:
                    raise GeneralAutoloadError(
                        f"Invalid entity type, can't attach '{type(entity)}' to the "
                        f"parent '{type(parent)}'"
                    )
            return entity

    def _has_same_module_id(self, module, module_id):
        if (
            module
            and module_id
            and (
                "module" in module.name.lower()
                and module.relative_address.native_index == module_id
            )
        ):
            return True
        return False

    def attach_port_to_parent(self, entity_port, if_port, port_id):
        parent = self.get_parent_module(port_id, entity_port)
        parent.connect_port(if_port)

    def _get_port_parent_ids_list(self, port_id):
        if "-" in port_id:
            port_ids = port_id.split("-")
        elif not port_id:
            port_ids = []
        else:
            port_ids = [port_id]
        return port_ids

    def get_entity_parent_entity(self, entity):
        parent_index = self._physical_table_service.parent_dict.get(entity)
        if parent_index:
            return self._physical_table_service.physical_chassis_dict.get(
                parent_index
            ) or self._physical_table_service.create_module(parent_index)

    def generate_module(self, module_id):
        module_object = self._resource_model.entities.Module(index=module_id)
        return module_object

    def generate_sub_module(self, module_id):
        module_object = self._resource_model.entities.SubModule(index=module_id)
        return module_object
