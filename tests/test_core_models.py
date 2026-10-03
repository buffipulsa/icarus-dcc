import pytest

from icarus_dcc.core import ApplicationIdentity, PipelineContext


def test_application_identity_requires_name_and_version() -> None:
    assert ApplicationIdentity("Maya", "2024").version == "2024"

    with pytest.raises(ValueError, match="Application name"):
        ApplicationIdentity(" ", "2024")


def test_pipeline_context_requires_all_parts() -> None:
    context = PipelineContext("demo", "character_hero", "rig")

    assert context.entity == "character_hero"

    with pytest.raises(ValueError, match="task"):
        PipelineContext("demo", "character_hero", "")
