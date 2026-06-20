"""JSON serialization helpers for UV delta transfer maps."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from icarus_dcc.uv_delta_transfer.records import TransferMap, TransferMapRecord


def transfer_map_to_dict(transfer_map: TransferMap) -> dict[str, Any]:
    """Return a JSON-compatible dictionary for a transfer map."""

    return {
        "low_mesh": transfer_map.low_mesh,
        "high_mesh": transfer_map.high_mesh,
        "uv_set": transfer_map.uv_set,
        "records": [
            {
                "high_vertex_id": record.high_vertex_id,
                "low_face_id": record.low_face_id,
                "low_vertex_ids": list(record.low_vertex_ids),
                "barycentric": list(record.barycentric),
            }
            for record in transfer_map.records
        ],
    }


def transfer_map_from_dict(data: dict[str, Any]) -> TransferMap:
    """Build a transfer map from a decoded JSON dictionary."""

    return TransferMap(
        low_mesh=data["low_mesh"],
        high_mesh=data["high_mesh"],
        uv_set=data.get("uv_set", "map1"),
        records=tuple(
            TransferMapRecord(
                high_vertex_id=record["high_vertex_id"],
                low_face_id=record["low_face_id"],
                low_vertex_ids=tuple(record["low_vertex_ids"]),
                barycentric=tuple(record["barycentric"]),
            )
            for record in data.get("records", ())
        ),
    )


def dumps_transfer_map(transfer_map: TransferMap, *, indent: int = 2) -> str:
    """Serialize a transfer map to a JSON string."""

    return json.dumps(transfer_map_to_dict(transfer_map), indent=indent, sort_keys=True)


def loads_transfer_map(payload: str) -> TransferMap:
    """Deserialize a transfer map from a JSON string."""

    data = json.loads(payload)
    if not isinstance(data, dict):
        msg = "transfer map JSON must decode to an object."
        raise TypeError(msg)

    return transfer_map_from_dict(data)


def save_transfer_map(path: str | Path, transfer_map: TransferMap) -> None:
    """Write a transfer map to a JSON file."""

    Path(path).write_text(dumps_transfer_map(transfer_map), encoding="utf-8")


def load_transfer_map(path: str | Path) -> TransferMap:
    """Read a transfer map from a JSON file."""

    return loads_transfer_map(Path(path).read_text(encoding="utf-8"))
