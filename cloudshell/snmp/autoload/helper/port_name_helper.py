from cloudshell.snmp.autoload.constants.port_constants import CS_NOT_ALLOWED_STR_PATTERN


def convert_port_name(port_name, replace_to="") -> str:
    result = port_name.replace("/", "-")
    return CS_NOT_ALLOWED_STR_PATTERN.sub(replace_to, result)
