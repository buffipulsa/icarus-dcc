# Changelog

All notable changes to this project will be documented in this file.

This changelog tracks project-facing changes, not local workstation setup steps.

## [Unreleased]

### Added

- Added UV-based Python development setup with Python 3.10 compatibility.
- Added Rez package definitions for `maya-2024`, `icarus_dcc`, and `icarus_dcc_maya`.
- Added initial development and Rez setup documentation.
- Added an external PySide launcher scaffold under `tools/launcher`.

### Changed

- Organized the project around DCC tooling rather than a Maya-only development layout.
- Split Qt dependencies so `PySide6` supports the external launcher and `PySide2` supports Maya 2024 development IntelliSense.
- Kept local Rez installs, local configs, editor settings, and assistant tooling out of Git.