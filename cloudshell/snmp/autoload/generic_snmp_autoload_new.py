#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from cloudshell.snmp.autoload.exceptions.snmp_autoload_error import GeneralAutoloadError
from cloudshell.snmp.autoload.helper.snmp_autoload_helper import log_autoload_details
from cloudshell.snmp.autoload.system_info_table import SnmpSystemInfo


class GenericSNMPAutoload:
    def __init__(self, snmp_handler, logger):
        """Basic init with snmp handler and logger.

        :param snmp_handler:
        :param logger:
        :return:
        """
        self.snmp_handler = snmp_handler
        self.logger = logger
        self.elements = {}
        self._entity_table = None
        self._system_info = None
        self._validate_module_id_by_port_name = False
        self._discover_device()

    @property
    def port_table_service(self):
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

    def _discover_device(self):
        """General entry point for autoload.

        Read device structure and attributes: chassis, modules, submodules, ports,
        port-channels and power supplies
        :type resource_model: cloudshell.shell.standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        :param str supported_os:
        :param bool validate_module_id_by_port_name:
        :return: AutoLoadDetails object
        """
