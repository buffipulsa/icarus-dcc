"""Dependency-free plugin boundary for the Icarus host."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


class PluginError(RuntimeError):
    """Base exception for plugin host errors."""


class PluginRegistrationError(PluginError):
    """Raised when a plugin cannot be registered with a host."""


@dataclass(frozen=True)
class PluginDescriptor:
    """Stable identity and human-readable metadata for a plugin."""

    name: str
    version: str
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Plugin name cannot be empty.")
        if not self.version.strip():
            raise ValueError("Plugin version cannot be empty.")


@runtime_checkable
class Plugin(Protocol):
    """Contract implemented by an independently packaged Icarus plugin."""

    @property
    def descriptor(self) -> PluginDescriptor:
        """Return the plugin's identity and metadata."""

    def register(self, host: PluginHost) -> None:
        """Register plugin-owned capabilities with ``host``."""


class PluginHost:
    """Manage plugin lifecycle and the host-local capability registry."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}
        self._capabilities: dict[str, object] = {}

    @property
    def plugins(self) -> tuple[PluginDescriptor, ...]:
        """Return registered plugin descriptors in registration order."""

        return tuple(plugin.descriptor for plugin in self._plugins.values())

    def register_plugin(self, plugin: Plugin) -> None:
        """Register one plugin and invoke its registration hook."""

        descriptor = plugin.descriptor
        if descriptor.name in self._plugins:
            raise PluginRegistrationError(f'Plugin "{descriptor.name}" is already registered.')

        capability_names = set(self._capabilities)
        try:
            plugin.register(self)
        except Exception as error:
            for capability_name in set(self._capabilities) - capability_names:
                del self._capabilities[capability_name]
            raise PluginRegistrationError(
                f'Plugin "{descriptor.name}" failed during registration.'
            ) from error

        self._plugins[descriptor.name] = plugin

    def load_plugins(self, plugins: Iterable[Plugin]) -> None:
        """Register plugins in iterable order."""

        for plugin in plugins:
            self.register_plugin(plugin)

    def register_capability(self, name: str, capability: object) -> None:
        """Expose a plugin-owned capability under a host-local name."""

        if not name.strip():
            raise ValueError("Capability name cannot be empty.")
        if name in self._capabilities:
            raise PluginRegistrationError(f'Capability "{name}" is already registered.')
        self._capabilities[name] = capability

    def get_capability(self, name: str) -> object:
        """Return a registered capability by name."""

        try:
            return self._capabilities[name]
        except KeyError as error:
            raise KeyError(f'No capability is registered as "{name}".') from error

    def has_plugin(self, name: str) -> bool:
        """Return whether a plugin with ``name`` is registered."""

        return name in self._plugins
