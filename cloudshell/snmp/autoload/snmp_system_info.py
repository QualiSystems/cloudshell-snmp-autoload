import re

from cloudshell.shell.flows.autoload.autoload_utils import get_device_name

from cloudshell.snmp.autoload.domain.snmpv2_data import SnmpV2MibData


class SnmpSystemInfo(object):
    DEVICE_MODEL_PATTERN = re.compile(r"::(?P<model>\S+$)")
    VENDOR_OID_PATTERN = re.compile(r"1.3.6.1.4.1.\d+")
    OS_VERSION_PATTERN = re.compile(r"Version (?P<os_version>[^\s,]+)")

    def __init__(self, snmp_handler, logger, vendor=None):
        self._vendor = vendor
        self._snmp_handler = snmp_handler
        self._logger = logger
        self._device_model_pattern = self.DEVICE_MODEL_PATTERN
        self._os_version_pattern = self.OS_VERSION_PATTERN
        self._device_model_map_path = None
        self._snmp_v2_obj = SnmpV2MibData(snmp_handler, logger)

    def set_model_name_map_file_path(self, file_path):
        if file_path:
            self._device_model_map_path = file_path

    def set_device_model_pattern(self, device_model_pattern):
        if isinstance(device_model_pattern, str):
            self._device_model_pattern = re.compile(device_model_pattern)
        elif device_model_pattern:
            self._device_model_pattern = device_model_pattern

    def set_os_version_pattern(self, os_version_pattern):
        if isinstance(os_version_pattern, str):
            self._os_version_pattern = re.compile(os_version_pattern)
        elif os_version_pattern:
            self._os_version_pattern = os_version_pattern

    def is_valid_device_os(self, supported_os):
        """Validate device OS using snmp.

        :param supported_os: list of str or re._pattern_type.
            Certain regexp pattern to identify exact device OS.
        :return: True or False
        """
        supported_os_pattern = supported_os
        if isinstance(supported_os_pattern, str):
            supported_os_pattern = re.compile(
                supported_os_pattern, re.IGNORECASE | re.DOTALL
            )
        if isinstance(supported_os_pattern, list):
            supported_os_pattern = re.compile(
                "|".join(supported_os_pattern), re.IGNORECASE | re.DOTALL
            )

        system_description = self._snmp_v2_obj.get_system_description()
        self._logger.debug(
            "Detected system description: '{0}'".format(system_description)
        )
        if system_description:
            result = supported_os_pattern.search(str(system_description))

            if result:
                return True
            else:
                error_message = (
                    "Incompatible driver! Please use this driver for '{0}' "
                    "operation system(s)".format(supported_os_pattern.pattern)
                )
        else:
            error_message = "Unable to identify device firmware type"

        self._logger.error(error_message)
        return False

    def _get_device_model(self):
        """Get device model from the SNMPv2 mib.

        :return: device model
        :rtype: str
        """
        result = ""
        sys_obj_id = str(self._snmp_v2_obj.get_system_object_id())
        match_name = self._device_model_pattern.search(sys_obj_id)
        if match_name:
            result = match_name.group("model").capitalize()

        return result

    def _get_vendor(self):
        """Get device model from the SNMPv2 mib.

        :return: device model
        :rtype: str
        """
        if not self._vendor:
            sys_obj_id = self._snmp_v2_obj.get_system_object_id()
            sys_obj_id_oid = ".".join(map(str, sys_obj_id.raw_value))
            oid_match = self.VENDOR_OID_PATTERN.search(sys_obj_id_oid)
            if oid_match:
                self._vendor = self._snmp_handler.translate_oid(
                    oid_match.group()
                ).capitalize()

        return self._vendor

    def _get_device_os_version(self):
        """Get device OS Version form snmp SNMPv2 mib.

        :return: device model
        :rtype: str
        """
        result = ""
        matched = self._os_version_pattern.search(
            str(self._snmp_v2_obj.get_system_description())
        )
        if matched:
            result = matched.groupdict().get("os_version", "")
        return result

    def fill_attributes(self, resource):
        """Get root element attributes.

        :type resource: cloudshell.shell_standards.autoload_generic_models.GenericResourceModel  # noqa: E501
        """
        self._logger.debug("Building Root started")

        resource.contact_name = self._snmp_v2_obj.get_system_contact()
        resource.system_name = self._snmp_v2_obj.get_system_name()
        resource.location = self._snmp_v2_obj.get_system_location()
        resource.os_version = self._get_device_os_version()
        vendor = self._get_vendor()
        resource.vendor = vendor

        raw_model = self._get_device_model()
        model = re.sub(r"^{}".format(vendor), "", raw_model, flags=re.IGNORECASE)
        resource.model = model
        resource.model_name = self._get_model_name(raw_model)

        self._logger.info("Building Root completed")

    def _get_model_name(self, model):
        if self._device_model_map_path:
            return (
                get_device_name(file_name=self._device_model_map_path, sys_obj_id=model)
                or model
            )
