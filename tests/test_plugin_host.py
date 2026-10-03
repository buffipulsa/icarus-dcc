import pytest

from icarus_dcc.host import PluginDescriptor, PluginHost, PluginRegistrationError


class ExamplePlugin:
    descriptor = PluginDescriptor("example", "1.0.0")

    def register(self, host: PluginHost) -> None:
        host.register_capability("example.greeting", "hello")


class FailingPlugin:
    descriptor = PluginDescriptor("failing", "1.0.0")

    def register(self, host: PluginHost) -> None:
        host.register_capability("failing.partial", object())
        raise RuntimeError("registration failed")


def test_plugin_registers_capabilities() -> None:
    host = PluginHost()

    host.register_plugin(ExamplePlugin())

    assert host.has_plugin("example")
    assert host.get_capability("example.greeting") == "hello"


def test_failed_registration_rolls_back_capabilities() -> None:
    host = PluginHost()

    with pytest.raises(PluginRegistrationError, match="failing"):
        host.register_plugin(FailingPlugin())

    assert not host.has_plugin("failing")
    with pytest.raises(KeyError):
        host.get_capability("failing.partial")
