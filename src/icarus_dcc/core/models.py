"""Small, DCC-independent models shared by host adapters."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationIdentity:
    """Identify a host application and its version."""

    name: str
    version: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Application name cannot be empty.")
        if not self.version.strip():
            raise ValueError("Application version cannot be empty.")


@dataclass(frozen=True)
class PipelineContext:
    """Identify the pipeline location currently represented by a host session."""

    project: str
    entity: str
    task: str

    def __post_init__(self) -> None:
        for field_name, value in (
            ("project", self.project),
            ("entity", self.entity),
            ("task", self.task),
        ):
            if not value.strip():
                raise ValueError(f"Pipeline context {field_name} cannot be empty.")
