from dataclasses import dataclass

import pytest

from icarus_dcc.host import PluginDescriptor, PluginHost, PluginRegistrationError


@dataclass
class ExamplePlugin:
    descriptor: PluginDescriptor

    def register(self, host: PluginHost) -> None:
        host.register_capability("example.action", self)


def test_host_registers_external_plugin_and_capability() -> None:
    host = PluginHost()
    plugin = ExamplePlugin(PluginDescriptor("example", "1.0"))

    host.register_plugin(plugin)

    assert host.plugins == (plugin.descriptor,)
    assert host.has_plugin("example")
    assert host.get_capability("example.action") is plugin


def test_host_rejects_duplicate_plugin_names() -> None:
    host = PluginHost()
    host.register_plugin(ExamplePlugin(PluginDescriptor("example", "1.0")))

    with pytest.raises(PluginRegistrationError, match="already registered"):
        host.register_plugin(ExamplePlugin(PluginDescriptor("example", "2.0")))


def test_host_wraps_plugin_registration_failures() -> None:
    class BrokenPlugin:
        descriptor = PluginDescriptor("broken", "1.0")

        def register(self, host: PluginHost) -> None:
            host.register_capability("broken.action", self)
            raise RuntimeError("plugin problem")

    host = PluginHost()
    with pytest.raises(PluginRegistrationError, match="failed during registration"):
        host.register_plugin(BrokenPlugin())

    with pytest.raises(KeyError):
        host.get_capability("broken.action")


def test_plugin_descriptor_requires_identity() -> None:
    with pytest.raises(ValueError, match="name"):
        PluginDescriptor(" ", "1.0")

    with pytest.raises(ValueError, match="version"):
        PluginDescriptor("example", " ")
