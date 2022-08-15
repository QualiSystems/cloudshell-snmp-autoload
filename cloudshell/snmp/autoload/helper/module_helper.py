class ModuleHelper:
    def __init__(self, resource_model, physical_table_service, logger):
        self._resource_model = resource_model
        self._physical_table_service = physical_table_service
        self._logger = logger

    def attach_port_to_parent(self, entity_port, if_port, port_id):
        parent = self._physical_table_service.get_port_parent_entity(entity_port)
        parent = self._detect_and_connect_parent(parent)
        if parent:
            if (
                len(port_id.split("-")) - len(str(parent.relative_address).split("/"))
                > 1
            ):
                parent = (
                    self._physical_table_service.generate_module(parent, port_id)
                    or parent
                )
            parent.connect_port(if_port)
            self._update_parent_ids(parent, port_id)
            return parent

    def generate_module(self, parent_module, port_ids):
        port_ids_list = port_ids.split("-")
        chassis = port_ids_list[0]
        module_id = port_ids_list[1]
        sub_module = port_ids_list[2]
        sub_module_id = f"{chassis}-" f"{module_id}-" f"{sub_module}"

        module_object = self._resource_model.entities.SubModule(index=sub_module)
        self._physical_table_service.physical_modules_ids_dict[
            sub_module_id
        ] = module_object
        module_object.relative_address.parent_node = parent_module.relative_address
        parent_module.extract_sub_resources().append(module_object)
        return module_object

    def _update_parent_ids(self, parent, port_id):
        port_ids = port_id.split("-")[:-1]
        parent_ids = str(parent.relative_address).split("/")
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
            if chassis == port_ids[0]:
                parent.relative_address.native_index = port_ids[1]
                return
            else:
                parent.relative_address.native_index = port_ids[0]

    def _detect_and_connect_parent(self, entity):
        parent = self._physical_table_service.get_parent_entity(entity)
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
            self._detect_and_connect_parent(parent)
        return entity
