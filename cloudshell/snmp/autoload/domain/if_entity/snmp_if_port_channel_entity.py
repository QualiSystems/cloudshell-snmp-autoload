from cloudshell.snmp.autoload.domain.if_entity.snmp_if_entity import SnmpIfEntity


class SnmpIfPortChannel(SnmpIfEntity):
    def __init__(self, snmp_handler, logger, port_name_response, port_attributes_snmp_tables, name=None):
        super(SnmpIfPortChannel, self).__init__(snmp_handler, logger, port_name_response, port_attributes_snmp_tables)
        self._port_channel_associated_port = ""
        self._if_name = name

    @property
    def associated_port_list(self):
        if not self._port_channel_associated_port:
            self._port_channel_associated_port = self._get_associated_ports()
        return self._port_channel_associated_port

    def _get_associated_ports(self):
        """Get all ports associated with provided port channel
        :return:
        """

        result = []
        for key, value in self._port_attributes_snmp_tables.port_channel_ports.iteritems():
            if str(self.if_index) in value['dot3adAggPortAttachedAggID']:
                result.append(key)
        return result
