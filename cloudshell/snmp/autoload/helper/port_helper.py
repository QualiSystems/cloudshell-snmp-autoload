from __future__ import annotations

from typing import TYPE_CHECKING

from cloudshell.snmp.autoload.helper.module_helper import ModuleHelper
from cloudshell.snmp.autoload.snmp.entities.snmp_entity_base import BaseEntity

if TYPE_CHECKING:
    from logging import Logger

    from cloudshell.snmp.autoload.services.physical_entities_table import PhysicalTable
    from cloudshell.snmp.autoload.services.port_mapping_table import PortMappingService
    from cloudshell.snmp.autoload.services.port_table import PortsTable


class PortHelper:
    def __init__(
        self,
        physical_table_service: PhysicalTable,
        port_table_service: PortsTable,
        port_mapping_table_service: PortMappingService,
        resource_model,
        logger: Logger,
    ):
        """Init.

        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        """
        self._chassis = physical_table_service.physical_chassis_dict
        self._physical_table_service = physical_table_service
        self._port_table_service = port_table_service
        self._port_mapping_service = port_mapping_table_service
        self._resource_model = resource_model
        self._module_helper = ModuleHelper(
            resource_model, physical_table_service, logger
        )
        self._logger = logger
        self._identified_ports = []

    def build_ports_structure(self) -> None:
        """Get ports data.

        Get resource details and attributes for every port
        base on data from IF-MIB Table.
        """
        self._logger.info("Loading Ports ...")

        if self._port_table_service.ports_dict:
            if (
                self._port_mapping_service.port_mapping.port_mapping_snmp_table
            ):  # Build ports based on Entity-MIB
                self._load_ports_based_on_mapping()

            if len(self._port_table_service.ports_dict) == len(self._identified_ports):
                return
            self._load_ports_from_if_table()

        elif self._physical_table_service.physical_ports_list:
            self._load_ports_from_physical_table()

        self._logger.info("Building Ports completed")

    def _load_ports_based_on_mapping(self):
        for (
            if_index,
            phys_port_index,
        ) in self._port_mapping_service.port_mapping.port_mapping_snmp_table.items():
            phys_port = self._physical_table_service.physical_structure_table.get(
                phys_port_index
            )  # Port from resource_model based on Entity table
            phys_port_entity = self._physical_table_service.load_entity(
                phys_port_index
            )  # BaseEntity used for mapping
            if_port = self._port_table_service.ports_dict.get(
                if_index
            )  # Port from resource_model based on IF table

            if (
                not phys_port_entity
                or not if_port
                # or not phys_port
                or (phys_port_entity and not self._is_valid_port(phys_port_entity))
            ):
                self._identified_ports.append(if_index)
                continue
            if not phys_port:
                continue

            port_if_entity = self._port_table_service.load_if_port(if_index)
            port_id = port_if_entity.port_id
            port_ids = ""
            if port_id and "-" in port_id:
                port_ids = port_id[: port_id.rfind("-")]

            if len(port_ids.split("-")) > 3:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._module_helper.port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(if_port)
                self._identified_ports.append(if_index)
                continue

            self._module_helper.attach_port_to_parent(phys_port, if_port, port_ids)
            self._identified_ports.append(if_index)

    def _load_ports_from_if_table(self):
        for if_index, interface in self._port_table_service.ports_dict.items():
            if if_index in self._identified_ports:
                continue

            port_if_entity = self._port_table_service.load_if_port(if_index)
            sec_name = port_if_entity.if_descr_name
            port_id = port_if_entity.port_id
            if port_id is None:
                self._identified_ports.append(if_index)
                continue
            port_ids = port_id[: port_id.rfind("-")]
            if len(port_id.split("-")) > 4:
                port_ids = port_ids[: port_ids.rfind("-")]
            parent = self._module_helper.port_id_to_module_map.get(port_ids)
            if parent:
                parent.connect_port(interface)
                self._identified_ports.append(if_index)
                continue
            if self._physical_table_service.physical_ports_list:
                entity_port = self._port_mapping_service.get_mapping(
                    interface, sec_name
                )

                if entity_port:
                    phys_port_index = entity_port.relative_address.native_index
                    phys_port_entity = self._physical_table_service.load_entity(
                        phys_port_index
                    )
                    if self._is_valid_port(phys_port_entity):
                        self._module_helper.attach_port_to_parent(
                            entity_port, interface, port_ids
                        )
                        self._identified_ports.append(if_index)
                        continue
                    else:
                        continue
            parent = self._module_helper.get_parent_module(port_ids)
            parent.connect_port(interface)
            self._identified_ports.append(if_index)

    def _load_ports_from_physical_table(self):
        for phys_port_id in self._physical_table_service.physical_ports_list:
            phys_port = self._physical_table_service.physical_structure_table.get(
                phys_port_id
            )
            parent = self._module_helper.get_parent_module("", phys_port)
            if phys_port.name == "Port":
                phys_port_entity = self._physical_table_service.load_entity(
                    phys_port_id
                )
                new_rel_path = self._module_helper.find_module_ids(parent)
                new_rel_path.append(phys_port_entity.position_id)
                phys_port.name += "-".join(new_rel_path)
            parent.connect_port(phys_port)

    def _is_valid_port(self, entity_port: BaseEntity):
        result = True
        if self._port_table_service.is_wrong_port(entity_port.name):
            result = False
        if self._port_table_service.is_wrong_port(entity_port.description):
            result = False
        return result
