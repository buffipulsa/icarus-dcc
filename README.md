# Icarus DCC

Icarus DCC is a cross-DCC pipeline interface. The first host integration will
target Autodesk Maya, with the architecture kept independent of any one DCC,
launcher, or environment manager.

The core package has no Rez or DCC runtime dependency. Host integrations and
environment providers are optional adapters that can be added independently.

## Development

Create the local development environment with `uv`:

```powershell
uv sync
uv run pytest
uv run ruff check .
```

The current foundation contains the DCC-independent core models and the public
host/plugin contract. Host integrations implement `HostAdapter` and own all
application-specific API calls; the core package never imports a DCC SDK.

The first adapter will target Maya. Other hosts can be added later without
making Maya, Rez, Houdini, Blender, or Unreal dependencies of the core package.
