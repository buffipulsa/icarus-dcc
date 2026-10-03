from pathlib import Path

from icarus_dcc.core import ApplicationIdentity, PipelineContext
from icarus_dcc.host import HostAdapter


class FakeHostAdapter:
    application = ApplicationIdentity("Test DCC", "1.0")

    def __init__(self) -> None:
        self.scene_path: Path | None = None
        self.context: PipelineContext | None = None

    def get_current_scene(self) -> Path | None:
        return self.scene_path

    def get_current_context(self) -> PipelineContext | None:
        return self.context

    def open_scene(self, scene_path: Path) -> None:
        self.scene_path = scene_path


def test_host_adapter_contract_is_implementable_without_dcc_dependencies() -> None:
    adapter = FakeHostAdapter()

    assert isinstance(adapter, HostAdapter)
    assert adapter.application.name == "Test DCC"
    assert adapter.get_current_scene() is None


def test_host_adapter_exposes_scene_and_context() -> None:
    adapter = FakeHostAdapter()
    adapter.context = PipelineContext("demo", "asset", "model")

    adapter.open_scene(Path("scenes/asset_model.ma"))

    assert adapter.get_current_scene() == Path("scenes/asset_model.ma")
    assert adapter.get_current_context() == PipelineContext("demo", "asset", "model")
