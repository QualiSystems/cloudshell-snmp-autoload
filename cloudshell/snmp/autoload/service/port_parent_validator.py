import re


class PortParentValidator(object):
    def __init__(self, logger):
        self._logger = logger

    def validate_port_parent_ids(self, port):
        self._logger.info("Start port {} parent modules id validation".format(port.name))
        parent_ids_list = self._get_port_parent_ids(port)
        parent_ids = "-".join(parent_ids_list)  # ["0", "11"]
        if re.search(parent_ids, port.name, re.IGNORECASE):
            return
        else:
            parent_ids_from_port_match = re.search(r"\d+(-\d+)*$", port.name, re.IGNORECASE)
            if parent_ids_from_port_match:
                parent_ids_from_port = parent_ids_from_port_match.group()  # ["0", "7", "0", "0"]
                parent_ids_from_port_list = parent_ids_from_port.split("-")[:-1]  # ["0", "7", "0"]
                if len(parent_ids_list) > 1:
                    if len(parent_ids_from_port_list) > len(parent_ids_list):  # len["0", "7", "0"] > len["0", "11"]
                        digits = len(parent_ids_from_port_list) - len(parent_ids_list)
                        parent_ids_from_port_list = parent_ids_from_port_list[:-digits]  # ["0", "7"]

                    self._set_port_parent_ids(port, parent_ids_from_port_list)
        self._logger.info("Completed port {} parent modules id validation".format(port.name))

    def _set_port_parent_ids(self, port, port_parent_list):
        self._logger.info("Updating port parent modules ids".format(port.name))
        resource_element = port.relative_address.parent_node
        port_list = list(port_parent_list)
        port_list.reverse()
        while resource_element.native_index and len(port_list) > 1:
            resource_element.native_index = port_list[0]
            port_list.remove(resource_element.native_index)
            resource_element = resource_element.parent_node

    def _get_port_parent_ids(self, port):
        self._logger.info("Loading port parent modules ids".format(port.name))
        resource_element = port.relative_address.parent_node
        response = []
        while resource_element.native_index:
            response.append(resource_element.native_index)
            resource_element = resource_element.parent_node

        response.reverse()
        return response
