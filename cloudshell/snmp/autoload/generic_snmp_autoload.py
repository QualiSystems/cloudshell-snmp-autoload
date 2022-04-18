#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.snmp.autoload.core.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.helper.snmp_autoload_helper import log_autoload_details
from cloudshell.snmp.autoload.snmp_entity_table import SnmpEntityTable
from cloudshell.snmp.autoload.snmp_if_table import SnmpIfTable
from cloudshell.snmp.autoload.snmp_system_info import SnmpSystemInfo


class GenericSNMPAutoload(object):
    PORT_NAME_PATTERN = re.compile(r"\d+(/\d+)*", re.IGNORECASE)

    def __init__(self, snmp_handler, logger):
        """Basic init with snmp handler and logger.

        :param snmp_handler:
        :param logger:
        :return:
        """
        self.snmp_handler = snmp_handler
        self._resource_model = None
        self.logger = logger
        self.elements = {}
        self._entity_table = None
        self._system_info = None
        self._if_table = None
        self._validate_module_id_by_port_name = False
        self._if_ports_in_entity = False
        self._chassis = {}

    @property
    def if_table_service(self):
        if not self._if_table:
            self._if_table = SnmpIfTable(
                snmp_handler=self.snmp_handler, logger=self.logger
            )

        return self._if_table

    @property
    def entity_table_service(self):
        if not self._entity_table:
            self._entity_table = SnmpEntityTable(
                snmp_handler=self.snmp_handler,
                logger=self.logger,
                if_table=self.if_table_service,
            )
        return self._entity_table

    @property
    def system_info_service(self):
        if not self._system_info:
            self._system_info = SnmpSystemInfo(self.snmp_handler, self.logger)
        return self._system_info

    def load_mibs(self, path):
        """Loads mibs inside snmp handler."""
        self.snmp_handler.update_mib_sources(path)

    def discover(
        self, supported_os, resource_model, validate_module_id_by_port_name=False
    ):
        """General entry point for autoload. Read device structure and attributes: chassis, modules, submodules, ports, port-channels and power supplies.

        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        :param str supported_os:
        :param bool validate_module_id_by_port_name:
        :return: AutoLoadDetails object
        """
        self.entity_table_service.validate_module_id_by_port_name = (
            validate_module_id_by_port_name
        )
        if not resource_model:
            return
        self._resource_model = resource_model
        if not self.system_info_service.is_valid_device_os(supported_os):
            raise GeneralAutoloadError("Unsupported device OS")

        self.logger.info("*" * 70)
        self.logger.info("Start SNMP discovery process .....")
        self.system_info_service.fill_attributes(resource_model)

        entity_chassis_tree_dict = self.entity_table_service.chassis_structure_dict

        if entity_chassis_tree_dict:
            self._build_structure(entity_chassis_tree_dict.values(), resource_model)
            self._get_port_channels(resource_model)

        if not self._if_ports_in_entity:
            self._add_ports_from_iftable()

        autoload_details = resource_model.build(
            filter_empty_modules=True, use_new_unique_id=True
        )

        log_autoload_details(self.logger, autoload_details)
        return autoload_details

    def _build_structure(self, child_list, parent):
        for element in child_list:
            if isinstance(element.entity, SnmpEntityTable.ENTITY_CHASSIS):
                chassis = self._get_chassis_attributes(element, parent)
                self._chassis.update({str(element.entity.position_id): chassis})
                self._build_structure(element.child_list, chassis)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_MODULE):
                module = self._get_module_attributes(element, parent)
                if module:
                    self._build_structure(element.child_list, module)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_POWER_PORT):
                self._get_power_ports(element, parent)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_PORT):
                self._if_ports_in_entity = self._if_ports_in_entity or True
                self._get_ports_attributes(element.if_entity, parent)

    def _add_ports_from_iftable(self):
        """Get ports data.

        Get resource details and attributes for every port
        base on data from IF-MIB Table.
        """
        self.logger.info("Loading Ports ...")

        for if_index, interface in self.if_table_service.if_ports.items():
            if self.if_table_service.PORT_VALID_TYPE.search(interface.if_type):
                self.logger.debug("Trying to load port {}:".format(interface.port_name))
                match = re.search(
                    r"(?P<ch_index>\d+)(/\d+)*/(?P<if_index>\d+)$",
                    interface.if_descr_name,
                    re.IGNORECASE,
                )

                if match:
                    chassis_id = match.groupdict().get("ch_index")
                    if chassis_id not in self._chassis:
                        self._add_dummy_chassis(chassis_id)
                else:
                    chassis_id = next(iter(self._chassis), None)
                    if not chassis_id:
                        chassis_id = "0"
                        self._add_dummy_chassis(chassis_id)
                parent_element = self._chassis.get(chassis_id)
                self._get_ports_attributes(interface, parent_element)

        self.logger.info("Building Ports completed")

    def _add_dummy_chassis(self, chassis_id):
        """Create Dummy Chassis."""
        chassis_object = self._resource_model.entities.Chassis(index=chassis_id)

        self._resource_model.connect_chassis(chassis_object)
        self._chassis.update({str(chassis_id): chassis_object})
        self.logger.info("Added Dummy Chassis with index {}".format(chassis_id))

    def _get_chassis_attributes(self, chassis, parent):
        """Get Chassis element attributes.

        :type dict<str, cloudshell.snmp.autoload.snmp_entity_table.Element> chassis:
        """
        self.logger.debug("Building Chassis")
        if not chassis.entity:
            return

        chassis_object = self._resource_model.entities.Chassis(index=chassis.id)

        chassis_object.model = chassis.entity.model
        chassis_object.serial_number = chassis.entity.serial_number

        parent.connect_chassis(chassis_object)
        self.logger.info("Added " + chassis.entity.model + " Chassis")
        return chassis_object

    def _get_module_attributes(self, module, parent):
        """Set attributes for all discovered modules."""
        self.logger.debug("Building Modules")

        if isinstance(parent, self._resource_model.entities.Module):
            module_object = self._resource_model.entities.SubModule(index=module.id)
            parent.connect_sub_module(module_object)
        elif isinstance(parent, self._resource_model.entities.Chassis):
            module_object = self._resource_model.entities.Module(index=module.id)
            parent.connect_module(module_object)
        else:
            self.logger.error(
                "Failed to load the following element {}".format(parent.name)
            )
            return

        module_object.model = module.entity.model
        module_object.version = module.entity.os_version
        module_object.serial_number = module.entity.serial_number

        self.logger.info("Module {} added".format(module_object.model))
        return module_object

    def _get_power_ports(self, power_port, parent_element):
        """Get attributes for power ports provided in self.power_supply_list.

        :type power_port: cloudshell.snmp.autoload.snmp_entity_table.Element
        :return:
        """
        self.logger.debug("Building Power Port")
        power_port_object = self._resource_model.entities.PowerPort(index=power_port.id)
        power_port_object.model = power_port.entity.base_entity.model
        power_port_object.port_description = power_port.entity.base_entity.description
        power_port_object.version = power_port.entity.hardware_version
        power_port_object.serial_number = power_port.entity.serial_number
        parent_element.connect_power_port(power_port_object)
        self.logger.info(
            "Added "
            + power_port.entity.base_entity.model.strip(" \t\n\r")
            + " Power Port"
        )

    def _get_port_channels(self, parent_resource):
        """Get all port channels and set attributes for them.

        :type parent_resource: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        :return:
        """
        if not self.if_table_service.if_port_channels:
            return
        self.logger.info("Building Port Channels")
        for (
            if_port_channel_id,
            if_port_channel,
        ) in self.if_table_service.if_port_channels.items():
            interface_model = if_port_channel.port_name
            match_object = re.search(r"\d+$", interface_model)
            if match_object:
                interface_id = "{0}".format(match_object.group(0))
                associated_ports = ""
                for port in if_port_channel.associated_port_list:
                    if_port_name = self.if_table_service.get_if_entity_by_index(
                        port
                    ).if_name
                    associated_ports = (
                        if_port_name.replace("/", "-").replace(" ", "") + "; "
                    )

                port_channel = self._resource_model.entities.PortChannel(
                    index=interface_id
                )

                port_channel.associated_ports = associated_ports.strip(" \t\n\r")
                port_channel.port_description = if_port_channel.if_port_description
                port_channel.ipv4_address = if_port_channel.ipv4_address
                port_channel.ipv6_address = if_port_channel.ipv6_address

                parent_resource.connect_port_channel(port_channel)
                self.logger.info("Added " + interface_model + " Port Channel")

            else:
                self.logger.error(
                    "Adding of {0} failed. Name is invalid".format(interface_model)
                )

        self.logger.info("Building Port Channels completed")

    def _get_ports_attributes(self, port, parent_element):
        """Get resource details and attributes for every port in self.port_list."""
        name = port.port_name
        if not name:
            return

        self.logger.debug("Trying to load port {}:".format(port.port_name))

        port_object = self._resource_model.entities.Port(
            index=port.if_index, name=name.replace("/", "-")
        )
        port_object.mac_address = port.if_mac
        port_object.l2_protocol_type = port.if_type.replace("'", "")
        port_object.ipv4_address = port.ipv4_address
        port_object.ipv6_address = port.ipv6_address
        port_object.port_description = port.if_port_description
        port_object.bandwidth = port.if_speed
        port_object.mtu = port.if_mtu
        port_object.duplex = port.duplex
        port_object.adjacent = port.adjacent
        port_object.auto_negotiation = port.auto_negotiation
        port_object.mac_address = port.if_mac
        parent_element.connect_port(port_object)
        self.logger.info("Added {} Port".format(port.port_name))
