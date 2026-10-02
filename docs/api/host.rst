Host and plugins
================

The host API is intentionally independent of any optional tooling project.
External packages can implement the :class:`icarus_dcc.host.Plugin` contract
and register their capabilities with :class:`icarus_dcc.host.PluginHost`.

.. automodule:: icarus_dcc.host
    :members:
