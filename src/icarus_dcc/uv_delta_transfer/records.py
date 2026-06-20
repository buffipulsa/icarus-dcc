"""Data records for UV delta transfer maps."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

BarycentricWeights = tuple[float, float, float]
LowVertexIds = tuple[int, int, int]


def _as_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an integer."
        raise TypeError(msg)

    if value < 0:
        msg = f"{name} must be non-negative."
        raise ValueError(msg)

    return value


def _as_int_triplet(values: Sequence[object], name: str) -> LowVertexIds:
    if len(values) != 3:
        msg = f"{name} must contain exactly three values."
        raise ValueError(msg)

    return (
        _as_int(values[0], f"{name}[0]"),
        _as_int(values[1], f"{name}[1]"),
        _as_int(values[2], f"{name}[2]"),
    )


def _as_float_triplet(values: Sequence[object], name: str) -> BarycentricWeights:
    if len(values) != 3:
        msg = f"{name} must contain exactly three values."
        raise ValueError(msg)

    return (float(values[0]), float(values[1]), float(values[2]))


@dataclass(frozen=True, slots=True)
class TransferMapRecord:
    """Mapping from one high mesh vertex to a low mesh UV triangle sample."""

    high_vertex_id: int
    low_face_id: int
    low_vertex_ids: LowVertexIds
    barycentric: BarycentricWeights

    def __post_init__(self) -> None:
        object.__setattr__(self, "high_vertex_id", _as_int(self.high_vertex_id, "high_vertex_id"))
        object.__setattr__(self, "low_face_id", _as_int(self.low_face_id, "low_face_id"))
        object.__setattr__(
            self,
            "low_vertex_ids",
            _as_int_triplet(self.low_vertex_ids, "low_vertex_ids"),
        )
        object.__setattr__(
            self,
            "barycentric",
            _as_float_triplet(self.barycentric, "barycentric"),
        )

    def validate_barycentric_sum(self, tolerance: float = 1e-5) -> None:
        """Raise ValueError if barycentric weights do not approximately sum to 1."""

        weight_sum = sum(self.barycentric)
        if abs(weight_sum - 1.0) > tolerance:
            msg = (
                f"barycentric weights for high vertex {self.high_vertex_id} "
                f"must sum to 1.0 within {tolerance}."
            )
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class TransferMap:
    """Serializable UV delta transfer map."""

    low_mesh: str
    high_mesh: str
    uv_set: str = "map1"
    records: tuple[TransferMapRecord, ...] = ()

    def __post_init__(self) -> None:
        if not self.low_mesh:
            msg = "low_mesh must not be empty."
            raise ValueError(msg)
        if not self.high_mesh:
            msg = "high_mesh must not be empty."
            raise ValueError(msg)
        if not self.uv_set:
            msg = "uv_set must not be empty."
            raise ValueError(msg)

        object.__setattr__(
            self,
            "records",
            tuple(
                record
                if isinstance(record, TransferMapRecord)
                else TransferMapRecord(**record)  # type: ignore[arg-type]
                for record in self.records
            ),
        )

    def validate_record_count(self, high_vertex_count: int) -> None:
        """Raise ValueError if the map does not contain one record per high vertex."""

        if len(self.records) != high_vertex_count:
            msg = (
                f"transfer map has {len(self.records)} records, "
                f"but high mesh has {high_vertex_count} vertices."
            )
            raise ValueError(msg)

    def validate_barycentric_weights(self, tolerance: float = 1e-5) -> None:
        """Raise ValueError if any record has invalid barycentric weight sum."""

        for record in self.records:
            record.validate_barycentric_sum(tolerance=tolerance)
