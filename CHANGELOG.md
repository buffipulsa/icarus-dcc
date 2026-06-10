# Changelog

All notable changes to this project will be documented in this file.

This changelog tracks project-facing changes, not local workstation setup steps.

## [Unreleased]

### Added

- Added a `src` package layout for importable `icarus_dcc` launcher code.
- Added the initial launcher configuration model with typed config and settings records.
- Added pytest coverage for launcher config path derivation and settings loading.
- Added Sphinx as documentation tooling for future API docs.
- Added UV-based Python development setup with Python 3.10 compatibility.
- Added Rez package definitions for `maya-2024`, `icarus_dcc`, and `icarus_dcc_maya`.
- Added initial development and Rez setup documentation.

### Changed

- Updated VS Code settings for `src` package imports and cache-folder hiding.
- Added `scratch/` to ignored local development files.
- Organized the project around DCC tooling rather than a Maya-only development layout.
- Split Qt dependencies so `PySide6` supports the external launcher and `PySide2` supports Maya 2024 development IntelliSense.
- Kept local Rez installs, local configs, editor settings, and assistant tooling out of Git.
