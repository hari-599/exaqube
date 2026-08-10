from app.plugin.base import BasePlugin


class PluginRegistry:

    def __init__(self):
        self._plugins: dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> BasePlugin | None:
        return self._plugins.get(name)

    def all(self) -> list[BasePlugin]:
        return list(self._plugins.values())

    def tool_specs(self) -> list[dict]:
        return [plugin.tool_spec() for plugin in self._plugins.values()]