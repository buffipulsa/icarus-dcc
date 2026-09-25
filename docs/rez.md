# Rez Setup

Rez is used to describe runtime environments for DCC applications. It is not used as the project Python development environment.

## Local Infrastructure

Rez infrastructure should live outside the Git repository. A typical local layout is:

```text
<dcc-dev-root>/
  _rez/
    install/    Rez installation
    packages/   Local bound packages, such as python/platform/os/arch
    config/     Machine-local Rez config
  _python/      Standalone Python installs for infrastructure
  icarus-dcc/   This repository
```

The exact location is machine-specific. Do not commit the local Rez install, local package cache, or local config.

The repository contains commit-friendly package definitions:

```text
rez/packages/maya/2024
rez/packages/icarus_dcc/0.1.0
rez/packages/icarus_dcc_maya/0.1.0
```

## Activate Rez

In PowerShell, add your local Rez command directory to `PATH` and point Rez at your local config:

```powershell
$env:PATH = "<dcc-dev-root>\_rez\install\Scripts\rez;$env:PATH"
$env:REZ_CONFIG_FILE = "<dcc-dev-root>\_rez\config\rezconfig.py"
```

The local `rezconfig.py` should include both the local package repo and this project's package definitions:

```python
packages_path = [
    "<dcc-dev-root>/_rez/packages",
    "<dcc-dev-root>/icarus-dcc/rez/packages",
]

local_packages_path = "<dcc-dev-root>/_rez/packages"
release_packages_path = "<dcc-dev-root>/_rez/packages"
```

Use forward slashes in Rez config paths. This local config is intentionally ignored by Git.

## Maya 2024 Package

The `maya-2024` package expects this environment variable:

```powershell
$env:ICARUS_MAYA_2024_LOCATION = "<maya-2024-install-root>"
```

On a default Windows install, that value is usually:

```text
C:\Program Files\Autodesk\Maya2024
```

Then Maya can be launched with:

```powershell
rez env maya-2024 -- maya
```

## Package Intent

- `maya-2024` exposes an installed Maya runtime.
- `icarus_dcc` represents shared project paths.
- `icarus_dcc_maya` represents Maya-specific integration.

The current packages are intentionally small. Add paths only when the corresponding project folders exist.