from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginResult:
    plugin: str
    success: bool
    data: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)


class PluginContext:
    """
    Shared context between plugins during a single agent turn.
    """

    def __init__(self):
        self.memory: dict[str, Any] = {}


class BasePlugin(ABC):
    """
    Base class for every plugin.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    def accepts_upstream(self) -> tuple[str, ...]:
        """
        Plugins this plugin can consume output from.
        """
        return ()

    @abstractmethod
    async def execute(
        self,
        context: PluginContext,
        **kwargs,
    ) -> PluginResult:
        ...
    @abstractmethod
    def tool_spec(self) -> dict:
        return {
        "name": self.name,
        "description": self.description,
    }