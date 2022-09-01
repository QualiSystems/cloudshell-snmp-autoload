import re


class ModuleHelper:
    def __init__(self, resource_model, physical_table_service, logger):
        self._resource_model = resource_model
        self._physical_table_service = physical_table_service
        self._logger = logger
        self.port_id_to_module_map = {}

    def attach_port_to_parent(self, entity_port, if_port, port_id):
        parent = self.get_port_parent_entity(entity_port)
        if parent.name.lower().startswith("chassis"):
            parent.connect_port(if_port)
            return parent
        port_ids_list = self._get_port_parent_ids_list(port_id)
        if port_id and port_ids_list and len(port_ids_list) == 1:
            parent.relative_address.native_index = port_ids_list[0]
        if not parent:
            return
        parent = self.detect_and_connect_parent(parent)
        if parent:
            len_port_ids_list = len(port_ids_list)
            if (
                len_port_ids_list > 2
                and len_port_ids_list - len(str(parent.relative_address).split("/"))
                >= 1
            ):
                parent = self.generate_sub_module(parent, port_ids_list) or parent
            parent.connect_port(if_port)
            if len(port_ids_list) > 1:
                self._update_parent_ids(parent, port_id)
            return parent

    def _get_port_parent_ids_list(self, port_id):
        if "-" in port_id:
            port_ids = port_id.split("-")
        elif not port_id:
            port_ids = []
        else:
            port_ids = [port_id]
        return port_ids

    def _update_parent_ids(self, parent, port_id):
        port_ids = port_id.split("-")
        parent_ids = str(parent.relative_address).split("/")
        if len(port_ids) == len(parent_ids):
            parent_ids_list = re.findall(r"\d+", str(parent.relative_address))
            if port_ids == parent_ids_list:
                return
        relative_address = parent.relative_address
        chassis = parent_ids[0].replace("CH", "")
        if len(parent_ids) > 2:
            port_ids_list = port_ids[1:]
            if len(port_ids_list) > 2:
                port_ids_list = port_ids_list[:-1]
            port_ids_reverse = port_ids_list
            port_ids_reverse.reverse()
            for module_id in port_ids_reverse:
                relative_address.native_index = module_id
                relative_address = relative_address.parent_node
        elif len(parent_ids) == 2 and len(port_ids) > 1:
            if chassis and chassis == port_ids[0]:
                parent.relative_address.native_index = port_ids[1]
                return
            else:
                parent.relative_address.native_index = port_ids[0]
        else:
            parent.relative_address.native_index = port_ids[0]

    def detect_and_connect_parent(self, entity):
        if str(entity.relative_address.parent_node).startswith("CH"):
            return entity
        parent = self.get_parent_entity(entity)
        if parent and entity not in parent.extract_sub_resources():
            if "module" in parent.name.lower():
                new_entity = self._resource_model.entities.SubModule(
                    entity.relative_address.native_index
                )
                new_entity.serial_number = parent.serial_number
                new_entity.model = parent.model
                new_entity.version = parent.version
                entity = new_entity

            entity.relative_address.parent_node = parent.relative_address
            parent.extract_sub_resources().append(entity)
            if parent in self._physical_table_service.physical_chassis_dict.values():
                return entity
            new_entity = self.detect_and_connect_parent(parent)
            if new_entity.relative_address != entity.relative_address.parent_node:
                entity = new_entity
        return entity

    def get_port_parent_entity(self, entity_port):
        port_id = entity_port.relative_address.native_index
        parent_index = self._physical_table_service.port_parent_dict.get(port_id)
        parent = self._physical_table_service.physical_structure_table.get(parent_index)
        return parent

    def get_parent_entity(self, entity):
        if entity in self._physical_table_service.physical_chassis_dict.values():
            return
        entity_id = next(
            (
                k
                for k, v in self._physical_table_service.physical_structure_table.items()
                if v == entity
            ),
            None,
        )
        parent_entity = self._physical_table_service.find_parent_module(entity_id)
        parent = self._physical_table_service.physical_structure_table.get(
            parent_entity.index
        )
        return parent

    def get_parent_entity_by_ids(self, port_parent_id):
        result = self._get_parent_entity_by_ids(port_parent_id)
        return self.detect_and_connect_parent(result)

    def _get_parent_entity_by_ids(self, port_parent_id):
        if "-" in port_parent_id:
            module_parent = self.port_id_to_module_map.get(
                port_parent_id[: port_parent_id.rfind("-")]
            )
        else:
            module_parent = self.port_id_to_module_map.get(port_parent_id)
        if module_parent:
            sub_module = self.generate_sub_module(
                module_parent, port_parent_id.split("-")
            )
            return sub_module

        parent = self._physical_table_service.physical_modules_ids_dict.get(
            port_parent_id
        )
        if parent:
            return parent[0]
        if (
            not parent
            and len(self._physical_table_service.chassis_ids_dict) == 1
            and len(port_parent_id.split("-")) < 3
        ):
            chassis_id = list(self._physical_table_service.chassis_ids_dict.keys())[0]
            parent_id = f"{chassis_id}-{port_parent_id}"
            parent = self._get_physical_module(parent_id)
            if parent:
                return parent
        elif not parent and len(port_parent_id.split("-")) < 2:
            for chassis in self._physical_table_service.chassis_ids_dict:
                parent = self._physical_table_service.physical_modules_ids_dict.get(
                    f"{chassis}-{port_parent_id}"
                )
                if parent:
                    return parent[0]
        if not parent:
            parent = self._find_or_generate_parent(port_parent_id)
        return parent

    def _find_or_generate_parent(self, port_parent_id):
        ids = port_parent_id.split("-")
        parent = None
        if len(ids) == 1:
            parent = next(
                (
                    chassis
                    for chassis in self._physical_table_service.chassis_ids_dict.values()
                ),
                None,
            )
            chassis_id = parent.relative_address.native_index
            module_ids = f"{chassis_id}-{ids[0]}"
            module = self._get_physical_module(module_ids)
            return module or self.generate_module(parent, ids[0])
        elif len(ids) == 2:
            chassis_id, module_id = ids
            chassis = self._physical_table_service.chassis_ids_dict.get(chassis_id)
            parent_module = self._get_physical_module(f"{chassis_id}-{module_id}")
            if not parent_module:
                parent_module = self.generate_module(chassis, module_id)
            if not chassis:
                if len(self._physical_table_service.chassis_ids_dict) == 1:
                    chassis = next(
                        (
                            chassis
                            for chassis in self._physical_table_service.chassis_ids_dict.values()
                        ),
                        None,
                    )
                    module_id = chassis_id
                    chassis_id = chassis.relative_address.native_index

                    sub_module_ids = [chassis_id]
                    sub_module_ids.extend(ids)
                    sub_module = self._get_physical_module(sub_module_ids)
                    if sub_module:
                        return sub_module
                    parent_module = self._get_physical_module(
                        f"{chassis_id}-{module_id}"
                    )
                    if not parent_module:
                        parent_module = self.generate_module(chassis, module_id)
                    return self.generate_sub_module(parent_module, sub_module_ids)

            return parent_module
        elif len(ids) == 3:
            chassis_id, module_id, sub_module_id = ids
            parent = self._physical_table_service.physical_modules_ids_dict.get(
                f"{chassis_id}-{module_id}-{sub_module_id}"
            )
            if not parent:
                chassis = self._get_chassis(chassis_id)
                if not chassis:
                    raise Exception("Unknown modules detected")
                chassis_id = chassis.relative_address.native_index
                sub_module_ids = f"{chassis_id}-{module_id}-{sub_module_id}"
                sub_module = self._get_physical_module(sub_module_ids)
                if sub_module:
                    return sub_module
                parent_module = self._get_physical_module(f"{chassis_id}-{module_id}")
                if not parent_module:
                    parent_module = self.generate_module(chassis, module_id)
                sub_module_id = [chassis_id]
                sub_module_id.extend(ids[1:])
                parent = self.generate_sub_module(parent_module, sub_module_id)
            else:
                parent = parent[0]
        return parent

    def _get_physical_module(self, module_id):
        module = self.port_id_to_module_map.get(module_id)
        if module:
            return module
        module = self._physical_table_service.physical_modules_ids_dict.get(module_id)
        if module:
            return module[0]

    def _get_chassis(self, chassis_id):
        chassis = self._physical_table_service.chassis_ids_dict.get(chassis_id)
        if not chassis:
            if len(self._physical_table_service.chassis_ids_dict) == 1:
                chassis = next(
                    (
                        chassis
                        for _, chassis in self._physical_table_service.chassis_ids_dict.items()
                    ),
                    None,
                )
        return chassis

    def generate_module(self, parent_module, module_id):
        module_object = self._resource_model.entities.Module(index=module_id)
        # self._physical_table_service.physical_modules_ids_dict[
        #     module_id
        # ].append(module_object)
        module_object.relative_address.parent_node = parent_module.relative_address
        parent_module.extract_sub_resources().append(module_object)
        self._physical_table_service.physical_modules_ids_dict[module_id].append(
            module_object
        )
        return module_object

    def generate_sub_module(self, parent_module, port_ids_list):
        chassis = port_ids_list[0]
        module_id = port_ids_list[1]
        sub_module = port_ids_list[2]
        sub_module_id = f"{chassis}-" f"{module_id}-" f"{sub_module}"

        module_object = self._resource_model.entities.SubModule(index=sub_module)
        self._physical_table_service.physical_modules_ids_dict[sub_module_id].append(
            module_object
        )
        module_object.relative_address.parent_node = parent_module.relative_address
        parent_module.extract_sub_resources().append(module_object)
        return module_object
