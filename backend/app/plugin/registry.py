from app.plugin.decorators import PLUGIN_REGISTRY
from app.plugin.base import BasePlugin


class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, BasePlugin] = {}

        for plugin_cls in PLUGIN_REGISTRY.values():
            plugin = plugin_cls()
            self._plugins[plugin.name] = plugin

    def get(self, name: str) -> BasePlugin:
        return self._plugins[name]

    def list_plugins(self) -> list[str]:
        return list(self._plugins.keys())

    def tool_specs(self) -> list[dict]:
        return [
            {
                "name": plugin.name,
                "description": plugin.description,
            }
            for plugin in self._plugins.values()
        ]