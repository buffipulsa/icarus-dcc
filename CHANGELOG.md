# Changelog

All notable changes to this project will be documented in this file.

This changelog tracks project-facing changes, not local workstation setup steps.

## [Unreleased]

### Added

- Added GitHub Pages publishing for the Sphinx documentation.
- Added Sphinx API documentation for the Maya handles, launcher config,
  development reload helpers, logging helpers, and connection records.
- Added documentation build requirements and a GitHub Actions workflow that
  checks docs on pull requests and publishes them from `main`.
- Added Maya API 2.0 handles for dependency nodes, DAG nodes, and meshes.
- Added Maya integration tests for mesh shape resolution from transforms,
  intermediate meshes, invalid nodes, nested transforms, and instanced paths.
- Added initial Maya connection record scaffolding.
- Added package logging configuration helpers.
- Added dependency-aware module reloading helpers for Maya development.
- Added VS Code docstring spell checking configuration.
- Added empty UV model, importer, and exporter modules for the next transfer
  work.
- Added pure UV barycentric math helpers and tests for the UV delta transfer prototype.
- Added a `src` package layout for importable `icarus_dcc` launcher code.
- Added the initial launcher configuration model with typed config and settings records.
- Added pytest coverage for launcher config path derivation and settings loading.
- Added Sphinx as documentation tooling for future API docs.
- Added UV-based Python development setup with Python 3.10 compatibility.
- Added Rez package definitions for `maya-2024`, `icarus_dcc`, and `icarus_dcc_maya`.
- Added initial development and Rez setup documentation.

### Changed

- Updated the README with a link to the hosted documentation.
- Updated the mesh handle to resolve mesh shapes from transform nodes and bind
  inherited Maya handles to the resolved shape path.
- Updated Rez development packages to point at the local development sources.
- Updated wheel configuration formatting.
- Updated VS Code settings for `src` package imports and cache-folder hiding.
- Added `scratch/` to ignored local development files.
- Organized the project around DCC tooling rather than a Maya-only development layout.
- Split Qt dependencies so `PySide6` supports the external launcher and `PySide2` supports Maya 2024 development IntelliSense.
- Kept local Rez installs, local configs, editor settings, and assistant tooling out of Git.
