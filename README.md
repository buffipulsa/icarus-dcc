# Icarus DCC

Icarus DCC is an early-stage, open-source DCC-facing pipeline host focused first on Autodesk Maya. It provides stable host contracts and DCC utilities while allowing tooling to remain in independently packaged plugins.

## Goals

- Prototype Maya tools in Python with a structure that can later be ported to C++.
- Use Rez to describe and launch DCC runtime environments.
- Use uv for the local Python development environment used by VS Code, linting, tests, and type stubs.
- Document public Python modules with Sphinx and publish them through GitHub Pages.
- Use CMake later for compiled C++ Maya plug-ins.
- Keep machine-local install paths out of the Git repository.
- Keep optional pipeline tools outside the Icarus distribution; integrations belong in separate adapter packages.

## Host and Plugin Boundary

`icarus_dcc.host` contains the dependency-free public boundary for external
plugins. A plugin supplies a `PluginDescriptor` and a `register(host)` method;
the host manages lifecycle and plugin-owned capabilities.

Icarus does not import or require `emmTools` or `open-rig-graph`. Those projects
remain independent and may integrate through separately maintained optional
adapter packages.

## Current Tooling

| Tool | Purpose |
| --- | --- |
| uv | Project `.venv`, Python 3.10 dev tooling, `maya-stubs`, `pytest`, `ruff` |
| Rez | Runtime environment resolution and Maya launch packages |
| PySide6 | External desktop launcher UI |
| PySide2 | Maya 2024 UI development IntelliSense |
| Maya 2024 | Initial DCC target and compatibility baseline |
| CMake | Planned C++ plug-in build system |
| Sphinx | API documentation generated from NumPy-style docstrings |
| GitHub Actions | Documentation checks and GitHub Pages publishing |

## Repository Layout

```text
icarus-dcc/
  docs/                 Project setup, API docs, and Sphinx configuration
  plugins/              Future Maya plug-in code
  rez/                  Commit-friendly Rez package definitions
  src/icarus_dcc/       Importable Python package code
    dev/                Maya development reload helpers
    host/               Dependency-free host/plugin contracts
    launcher/           Launcher configuration records
    maya/               Maya API 2.0 node handles and records
    uv/                 UV delta transfer package scaffold
  tests/                Python test suite
  CHANGELOG.md          Project-facing change history
  pyproject.toml        UV-managed Python project metadata
  uv.lock               Locked Python development dependencies
```

Local infrastructure should live outside this repository:

```text
<dcc-dev-root>/
  _python/              Standalone Python installs for infrastructure
  _rez/                 Local Rez install, package repo, and local config
  icarus-dcc/           This repository
```

Those local infrastructure folders are intentionally not part of this Git repository.

## Quick Start

Create or refresh the UV environment:

```powershell
uv sync
```

Use this interpreter in VS Code:

```text
${workspaceFolder}\.venv\Scripts\python.exe
```

Activate Rez from your local setup:

```powershell
$env:PATH = "<dcc-dev-root>\_rez\install\Scripts\rez;$env:PATH"
$env:REZ_CONFIG_FILE = "<dcc-dev-root>\_rez\config\rezconfig.py"
```

Set the local Maya install path before resolving the Maya package:

```powershell
$env:ICARUS_MAYA_2024_LOCATION = "<maya-2024-install-root>"
```

On a default Windows Maya 2024 install, the Maya root is usually:

```text
C:\Program Files\Autodesk\Maya2024
```

Launch Maya through Rez:

```powershell
rez env maya-2024 -- maya
```

## Documentation

- [Online documentation](https://buffipulsa.github.io/icarus-dcc/)
- [Development setup](docs/development.md)
- [Rez setup](docs/rez.md)
- [Changelog](CHANGELOG.md)

Build the documentation locally with:

```powershell
uv run --no-project --python 3.10 --with-requirements docs/requirements.txt sphinx-build -b html -W --keep-going docs docs/_build/html
```

The published documentation is rebuilt automatically from `main`.

## Notes

This project intentionally keeps generated environments, local Rez installs, assistant state, and editor state out of Git. The committed Rez files are package definitions and examples of the environment design, not the local package cache or Rez installation itself.
