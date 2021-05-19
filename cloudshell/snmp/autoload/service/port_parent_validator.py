import re


class PortParentValidator(object):
    MIN_PORT_ID_LENGTH = 3  # Skipping Port names with less then 3 digits

    def __init__(self, logger):
        self._logger = logger

    def validate_port_parent_ids(self, port):
        name = port.if_entity.if_name or port.if_entity.if_descr_name
        self._logger.debug("Start port {} parent modules id validation".format(name))
        parent_ids = port.parent.full_id  # ["0", "11"]
        parent_ids_list = parent_ids.split("/")
        if re.search(parent_ids, name, re.IGNORECASE):
            self._logger.debug("Port {} parent modules ids are valid.".format(name))
            return
        else:
            parent_ids_from_port_match = re.search(r"\d+(/\d+)*$", name, re.IGNORECASE)
            if parent_ids_from_port_match:
                parent_ids_from_port = (
                    parent_ids_from_port_match.group()
                )  # ["0", "7", "0", "0"]
                parent_ids_from_port_list = parent_ids_from_port.split("/")
                if len(parent_ids_from_port_list) > len(parent_ids_list):  # > 1:
                    parent_ids_from_port_list = parent_ids_from_port_list[
                        : len(parent_ids_list)
                    ]  # ["0", "7"]

                    self._set_port_parent_ids(port, parent_ids_from_port_list)
                    self._logger.debug(
                        "Completed port {} parent modules id validation".format(name)
                    )
                else:
                    self._logger.debug(
                        "Failed to validate port {} parent modules ids. "
                        "Skipping.".format(name)
                    )

    def _set_port_parent_ids(self, port, port_parent_list):
        self._logger.debug("Updating port parent modules ids")
        resource_element = port.parent
        port_list = list(port_parent_list)
        while resource_element.parent:
            new_id = port_list.pop(-1)
            if new_id != resource_element.id:
                resource_element.id = new_id
            resource_element = resource_element.parent

    def _get_port_parent_ids(self, port):
        self._logger.debug("Loading port parent modules ids")
        resource_element = port.parent
        response = []
        while resource_element:
            response.append(resource_element.id)
            if not resource_element.parent:
                break
            resource_element = resource_element.parent

        response.reverse()
        return response
