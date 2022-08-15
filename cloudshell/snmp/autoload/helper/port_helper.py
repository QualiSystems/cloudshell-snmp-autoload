from cloudshell.snmp.autoload.helper.module_helper import ModuleHelper


class PortHelper:
    def __init__(
        self,
        physical_table_service,
        port_table_service,
        port_mapping_table_service,
        resource_model,
        logger,
    ):
        self._chassis = physical_table_service.physical_chassis_dict
        self._physical_table_service = physical_table_service
        self._port_table_service = port_table_service
        self._port_mapping_table_service = port_mapping_table_service
        self._resource_model = resource_model
        self._module_helper = ModuleHelper(
            resource_model, physical_table_service, logger
        )
        self._logger = logger
        self.identified_ports = []
        self._port_parent_ids_to_module_map = {}
        self._port_id_to_module_map = {}

    def load_ports_based_on_mapping(self):
        for (
            if_index,
            phys_port_index,
        ) in (
            self._port_mapping_table_service.port_mapping.port_mapping_snmp_table.items()
        ):
            phys_port = self._physical_table_service.physical_structure_table.get(
                phys_port_index
            )
            if not self._is_valid_port(phys_port):
                continue
            if_port = self._port_table_service.ports_dict.get(if_index)
            port_if_entity = self._port_table_service.load_if_port(if_index)
            port_id = port_if_entity.port_id
            port_ids = port_id[: port_id.rfind("-")]
            if len(port_ids.split("-")) > 3:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(if_port)
                self.identified_ports.append(if_index)
                continue

            parent = self._module_helper.attach_port_to_parent(
                phys_port, if_port, port_id
            )
            if not parent:
                continue
            self.identified_ports.append(if_index)
            if port_ids not in self._port_id_to_module_map:
                self._port_id_to_module_map[port_ids] = parent

    def load_ports_from_if_table(self):
        for if_index, interface in self._port_table_service.ports_dict.items():
            if if_index in self.identified_ports:
                continue

            port_if_entity = self._port_table_service.load_if_port(if_index)
            sec_name = port_if_entity.if_descr_name
            port_id = port_if_entity.port_id
            port_ids = port_id[: port_id.rfind("-")]
            if len(port_id.split("-")) > 4:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(interface)
                continue
            if self._physical_table_service.physical_ports_list:
                entity_port = self._port_mapping_table_service.get_mapping(
                    interface, sec_name
                )
                if not entity_port:
                    self._logger.debug(f"No mapping found for port {interface.name}")
                elif self._is_valid_port(entity_port):
                    self._module_helper.attach_port_to_parent(
                        entity_port, interface, port_id
                    )
                    self._port_id_to_module_map[port_ids] = parent
                    self.identified_ports.append(if_index)
                    continue
            self._guess_port_parent(if_index, interface)
            self.identified_ports.append(if_index)

    def load_ports_from_physical_table(self):
        for phys_port in self._physical_table_service.physical_ports_list:
            parent = self._physical_table_service.get_parent_entity(
                phys_port,
            )
            if parent:
                parent.connect_port(phys_port)

    def _guess_port_parent(self, if_index, interface):
        port_if_entity = self._port_table_service.load_if_port(if_index)
        port_id = port_if_entity.port_id
        port_ids = port_id[: port_id.rfind("-")]
        parent = self._physical_table_service.get_parent_entity_by_ids(port_ids)
        if parent:
            parent.connect_port(interface)
            self._port_id_to_module_map[port_ids] = parent
        else:
            self._add_port_to_chassis(interface, port_id)

    def _is_valid_port(self, entity_port):
        result = True
        if self._port_table_service.is_wrong_port(entity_port.name):
            result = False
        if entity_port.port_description and self._port_table_service.is_wrong_port(
            entity_port.port_description
        ):
            result = False
        return result

    def _add_port_to_chassis(self, interface, port_id):
        """Add port to chassis."""
        parent_element = None
        if len(self._chassis) > 1:
            if port_id:
                chassis_id = port_id.split("/")[0]
                parent_element = self._chassis.get(chassis_id, None)
        if not parent_element:
            if not self._chassis:
                chassis_id = "0"
                self._add_dummy_chassis(chassis_id)

        parent_element = next(iter(self._chassis.values()))
        parent_element.connect_port(interface)

    def _add_dummy_chassis(self, chassis_id):
        """Create Dummy Chassis."""
        chassis_object = self._resource_model.entities.Chassis(index=chassis_id)

        self._resource_model.connect_chassis(chassis_object)
        self._chassis.update({str(chassis_id): chassis_object})
        self._logger.info(f"Added Dummy Chassis with index {chassis_id}")
