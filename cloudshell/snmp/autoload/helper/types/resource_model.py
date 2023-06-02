from __future__ import annotations

from typing_extensions import Protocol


class ResourceModelProto(Protocol):
    entities: ResourceModelEntitiesProto

    def build(self):
        ...

    def connect_chassis(self, chassis: ResourceModelChassisProto) -> None:
        ...

    def connect_port_channel(self, port_channel: ResourceModelPortChanelProto) -> None:
        ...


class ResourceModelEntitiesProto(Protocol):
    Chassis: type[ResourceModelChassisProto]
    PortChannel: type[ResourceModelPortChanelProto]
    PowerPort: type[ResourceModelPowerPortProto]
    Module: type[ResourceModelModuleProto]
    SubModule: type[ResourceModelModuleProto]
    Port: type[ResourceModelPortProto]


class ResourceModelEntityProto(Protocol):
    def __init__(self, index: str, name: str | None = None):
        self.index = index
        self.name = name


class ResourceModelPortProto(ResourceModelEntityProto):
    ...


class ResourceModelPortChanelProto(ResourceModelEntityProto):
    ...


class ResourceModelChassisProto(ResourceModelEntityProto):
    def connect_power_port(self, power_port: ResourceModelPowerPortProto) -> None:
        ...

    def connect_port(self, port: ResourceModelPortProto) -> None:
        ...


class ResourceModelModuleProto(ResourceModelEntityProto):
    def connect_sub_module(self, sub_module: ResourceModelSubModuleProto) -> None:
        ...

    def connect_port(self, port: ResourceModelPortProto) -> None:
        ...


class ResourceModelSubModuleProto(ResourceModelEntityProto):
    def connect_port(self, port: ResourceModelPortProto) -> None:
        ...


class ResourceModelPowerPortProto(ResourceModelEntityProto):
    ...
