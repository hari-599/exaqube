PLUGIN_REGISTRY: dict[str, type] = {}


def register_plugin(cls):
    instance = cls()
    PLUGIN_REGISTRY[instance.name] = cls
    return cls