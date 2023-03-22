from abc import ABC, abstractmethod
from contextlib import suppress


class PortAttributesServiceInterface(ABC):
    def __init__(self, snmp_service, logger):
        self._snmp_service = snmp_service
        self._logger = logger
        self._thread_list = []

    @abstractmethod
    def load_snmp_table(self):
        pass

    def finalize_thread(self):
        with suppress(Exception):
            [thread.join(0) for thread in self._thread_list]
