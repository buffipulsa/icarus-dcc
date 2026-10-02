"""Public host and plugin contracts for Icarus DCC.

The host package intentionally depends only on the Python standard library.
External DCC tools can implement :class:`Plugin` and register themselves with
an :class:`PluginHost` without becoming part of the Icarus distribution.
"""

from .plugins import (
    Plugin,
    PluginDescriptor,
    PluginError,
    PluginHost,
    PluginRegistrationError,
)

__all__ = [
    "Plugin",
    "PluginDescriptor",
    "PluginError",
    "PluginHost",
    "PluginRegistrationError",
]
