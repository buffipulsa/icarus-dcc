"""Contracts implemented by integrations for individual DCC applications."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from icarus_dcc.core import ApplicationIdentity, PipelineContext


class HostAdapterError(RuntimeError):
    """Base exception for host operations."""


class SceneOperationError(HostAdapterError):
    """Raised when a host cannot complete a scene operation."""


@runtime_checkable
class HostAdapter(Protocol):
    """Dependency-free interface between Icarus and a DCC application.

    Implementations own all host-specific API calls. The Icarus core interacts
    only with this contract, allowing the same pipeline features to work with
    Maya, Houdini, Blender, Unreal, or another supported host.
    """

    @property
    def application(self) -> ApplicationIdentity:
        """Return the host application's identity."""

    def get_current_scene(self) -> Path | None:
        """Return the current scene path, if the host has a saved scene."""

    def get_current_context(self) -> PipelineContext | None:
        """Return the active pipeline context, if one is available."""

    def open_scene(self, scene_path: Path) -> None:
        """Open a scene in the host application."""
