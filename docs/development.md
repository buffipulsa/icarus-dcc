# Development Setup

This project uses two Python contexts on purpose.

## UV Development Environment

The project `.venv` is for local development only:

- VS Code interpreter
- Pylance autocomplete
- `maya-stubs`
- `pytest`
- `ruff`

Create or update it with:

```powershell
uv sync
```

The selected VS Code interpreter should be:

```text
${workspaceFolder}\.venv\Scripts\python.exe
```

This is not Maya's runtime Python. It is only the editor and tooling interpreter.

## Maya Runtime Python

Maya provides its own Python runtime when code runs inside Maya. The `.venv` can provide type information, but it cannot execute real `maya.cmds` or `maya.api.OpenMaya` outside Maya.

That means:

- Pure Python logic can be tested outside Maya.
- Maya API code should be tested inside Maya or `mayapy`.
- `maya-stubs` is for editor intelligence, not runtime behavior.

## Version Baseline

Maya 2024 is the first target, so project Python should stay compatible with Python 3.10. Avoid syntax and typing features that require newer Python versions unless the Maya 2024 target is dropped.

## C++ Direction

C++ support is planned through CMake. Python prototypes should stay simple and portable:

- explicit inputs and outputs
- direct loops
- simple data structures
- minimal dynamic behavior
- no Maya scene queries inside node compute paths

The goal is to make the eventual C++ version structurally similar to the Python prototype.