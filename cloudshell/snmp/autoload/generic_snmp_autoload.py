#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os

from cloudshell.snmp.autoload.core.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.helper.snmp_autoload_helper import log_autoload_details
from cloudshell.snmp.autoload.service.port_mapper import PortMappingService
from cloudshell.snmp.autoload.service.port_parent_validator import PortParentValidator
from cloudshell.snmp.autoload.snmp_entity_table import SnmpEntityTable
from cloudshell.snmp.autoload.snmp_general_info import SnmpGeneralInfo
from cloudshell.snmp.autoload.snmp_if_table import SnmpIfTable


class GenericSNMPAutoload(object):
    DEVICE_NAMES_MAP_FILE = os.path.join(os.path.dirname(__file__), os.pardir, "mibs", "device_names_map.csv")
    PORT_NAME_PATTERN = re.compile("\d+(/\d+)*", re.IGNORECASE)

    def __init__(self, snmp_handler, resource_config, logger):
        """Basic init with snmp handler and logger

        :param snmp_handler:
        :param logger:
        :return:
        """

        self.snmp_handler = snmp_handler
        self.shell_name = resource_config.shell_name
        self.shell_type = resource_config.family_name
        self.resource_name = resource_config.name
        self.logger = logger
        self.elements = {}
        self._port_mapping_service = None
        self._port_parent_validator_service = None
        self._entity_table = None
        self._if_table = None
        self._validate_module_id_by_port_name = False

    @property
    def if_table_service(self):
        if not self._if_table:
            self._if_table = SnmpIfTable(snmp_handler=self.snmp_handler, logger=self.logger)

        return self._if_table

    @property
    def entity_table_service(self):
        if not self._entity_table:
            self._entity_table = SnmpEntityTable(self.snmp_handler, self.logger)
        return self._entity_table

    @property
    def port_mapping_service(self):
        if not self._port_mapping_service:
            self._port_mapping_service = PortMappingService(self.if_table_service, self.logger)
        return self._port_mapping_service

    @property
    def port_parent_validator_service(self):
        if not self._port_parent_validator_service:
            self._port_parent_validator_service = PortParentValidator(self.logger)
        return self._port_parent_validator_service

    def load_mibs(self, path):
        """
        Loads mibs inside snmp handler

        """
        # path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mibs"))
        self.snmp_handler.update_mib_sources(path)

    def discover(self,
                 supported_os,
                 resource_model,
                 validate_module_id_by_port_name=False,
                 port_exclude_list=None):
        """General entry point for autoload,
        read device structure and attributes: chassis, modules, submodules, ports, port-channels and power supplies

        :type resource_model: cloudshell.shell_standards.autoload_generic_models.GenericResourceModel

        :return: AutoLoadDetails object
        """

        self.if_table_service.set_port_exclude_list(port_exclude_list)
        self._validate_module_id_by_port_name = validate_module_id_by_port_name
        if not resource_model:
            return
        self._resource_model = resource_model
        root_attributes = SnmpGeneralInfo(self.snmp_handler, self.logger)
        if not root_attributes.is_valid_device_os(supported_os):
            raise GeneralAutoloadError(self.__class__.__name__, 'Unsupported device OS')
        self.logger.info("*" * 70)
        self.logger.info("Start SNMP discovery process .....")
        root_attributes.fill_attributes(resource_model)

        entity_chassis_tree_dict = self.entity_table_service.chassis_structure_dict

        if entity_chassis_tree_dict:
            self._build_structure(entity_chassis_tree_dict.values(), resource_model)
            self._get_port_channels(resource_model)
        else:
            self.logger.error("Entity table error, no chassis found")

        autoload_details = resource_model.build()

        log_autoload_details(self.logger, autoload_details)
        return autoload_details

    def _build_structure(self, child_list, parent):
        """

        :type if_table: SnmpIfTable
        :type resource_model: cloudshell.shell_standards.autoload_generic_models.GenericResourceModel
        """
        for element in child_list:
            if isinstance(element.entity, SnmpEntityTable.ENTITY_CHASSIS):
                chassis = self._get_chassis_attributes(element, parent)
                self._build_structure(element.child_list, chassis)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_MODULE):
                module = self._get_module_attributes(element, parent)
                if module:
                    self._build_structure(element.child_list, module)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_POWER_PORT):
                self._get_power_ports(element, parent)

            elif isinstance(element.entity, SnmpEntityTable.ENTITY_PORT):
                self._get_ports_attributes(element, parent)

    def _get_chassis_attributes(self, chassis, parent):
        """ Get Chassis element attributes
        :type dict<str, cloudshell.snmp.autoload.snmp_entity_table.Element> chassis:
        """

        self.logger.info("Building Chassis")
        if not chassis.entity:
            return

        chassis_object = self._resource_model.entities.Chassis(index=chassis.id)

        chassis_object.model = chassis.entity.model
        chassis_object.serial_number = chassis.entity.serial_number

        parent.connect_chassis(chassis_object)
        self.logger.info("Added " + chassis_object.model + " Chassis")
        return chassis_object

    def _get_module_attributes(self, module, parent):
        """ Set attributes for all discovered modules """

        self.logger.info("Building Modules")

        if isinstance(parent, self._resource_model.entities.Module):
            module_object = self._resource_model.entities.SubModule(index=module.id)
            parent.connect_sub_module(module_object)
        elif isinstance(parent, self._resource_model.entities.Chassis):
            module_object = self._resource_model.entities.Module(index=module.id)
            parent.connect_module(module_object)
        else:
            self.logger.error("Failed to load the following element {}".format(parent.name))
            return

        module_object.model = module.entity.model
        module_object.version = module.entity.os_version
        module_object.serial_number = module.entity.serial_number

        self.logger.info("Module {} added".format(module_object.model))
        return module_object

    def _get_power_ports(self, power_port, parent_element):
        """Get attributes for power ports provided in self.power_supply_list

        :return:
        """

        self.logger.info("Building Power Port")
        power_port_object = self._resource_model.entities.PowerPort(index=power_port.id)
        power_port_object.model = power_port.entity.model
        power_port_object.port_description = power_port.entity.descirption
        power_port_object.version = power_port.entity.hardware_version
        power_port_object.serial_number = power_port.entity.serial_number
        parent_element.connect_power_port(power_port_object)
        self.logger.info("Added " + power_port_object.model.strip(" \t\n\r") + " Power Port")

    def _get_port_channels(self, parent_resource):
        """Get all port channels and set attributes for them

        :type parent_resource: cloudshell.shell_standards.autoload_generic_models.GenericResourceModel
        :type if_table: List<SnmpResponse>
        :return:
        """

        if not self.if_table_service.if_port_channels:
            return
        self.logger.info("Building Port Channels")
        for if_port_channel in self.if_table_service.if_port_channels:
            interface_model = if_port_channel.if_name
            match_object = re.search(r"\d+$", interface_model)
            if match_object:
                interface_id = "{0}".format(match_object.group(0))
                associated_ports = ""
                for port in if_port_channel.associated_port_list:
                    if_port_name = self.if_table_service.get_if_entity_by_index(port).if_name
                    associated_ports = if_port_name.replace('/', '-').replace(' ', '') + '; '

                port_channel = self._resource_model.entities.PortChannel(index=interface_id)

                port_channel.associated_ports = associated_ports.strip(' \t\n\r')
                port_channel.port_description = if_port_channel.if_port_description
                port_channel.ipv4_address = if_port_channel.ipv4_address
                port_channel.ipv6_address = if_port_channel.ipv6_address

                parent_resource.connect_port_channel(port_channel)
                self.logger.info("Added " + interface_model + " Port Channel")

            else:
                self.logger.error("Adding of {0} failed. Name is invalid".format(interface_model))

        self.logger.info("Building Port Channels completed")

    def _get_ports_attributes(self, entity_port, parent_element):
        """Get resource details and attributes for every port in self.port_list

        :return:
        """

        port = self.port_mapping_service.get_mapping(entity_port.entity)
        if not port:
            return

        if port.if_name == '':
            return

        self.logger.info("Trying to load port {}:".format(port.if_name))

        port_object = self._resource_model.entities.Port(index=entity_port.id,
                                                         name=port.if_name.value.replace("/", "-"))

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
        if self._validate_module_id_by_port_name:
            self.port_parent_validator_service.validate_port_parent_ids(port_object)
        self.logger.info("Added {} Port".format(port.if_name))
