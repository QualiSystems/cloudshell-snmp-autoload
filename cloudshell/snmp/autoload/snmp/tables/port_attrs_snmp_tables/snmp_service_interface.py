from abc import ABC, abstractmethod


class PortAttributesServiceInterface(ABC):
    @abstractmethod
    def load_snmp_table(self):
        pass
