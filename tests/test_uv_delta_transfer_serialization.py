from icarus_dcc.uv_delta_transfer.records import TransferMap, TransferMapRecord
from icarus_dcc.uv_delta_transfer.serialization import (
    dumps_transfer_map,
    loads_transfer_map,
    transfer_map_from_dict,
    transfer_map_to_dict,
)


def test_transfer_map_to_dict_matches_expected_json_shape():
    transfer_map = TransferMap(
        low_mesh="lowFace_geo",
        high_mesh="highFace_geo",
        uv_set="map1",
        records=(
            TransferMapRecord(
                high_vertex_id=0,
                low_face_id=128,
                low_vertex_ids=(12, 42, 43),
                barycentric=(0.2, 0.5, 0.3),
            ),
        ),
    )

    assert transfer_map_to_dict(transfer_map) == {
        "low_mesh": "lowFace_geo",
        "high_mesh": "highFace_geo",
        "uv_set": "map1",
        "records": [
            {
                "high_vertex_id": 0,
                "low_face_id": 128,
                "low_vertex_ids": [12, 42, 43],
                "barycentric": [0.2, 0.5, 0.3],
            }
        ],
    }


def test_transfer_map_from_dict_round_trips_records():
    transfer_map = transfer_map_from_dict(
        {
            "low_mesh": "lowFace_geo",
            "high_mesh": "highFace_geo",
            "uv_set": "map1",
            "records": [
                {
                    "high_vertex_id": 0,
                    "low_face_id": 128,
                    "low_vertex_ids": [12, 42, 43],
                    "barycentric": [0.2, 0.5, 0.3],
                }
            ],
        }
    )

    assert transfer_map == TransferMap(
        low_mesh="lowFace_geo",
        high_mesh="highFace_geo",
        uv_set="map1",
        records=(
            TransferMapRecord(
                high_vertex_id=0,
                low_face_id=128,
                low_vertex_ids=(12, 42, 43),
                barycentric=(0.2, 0.5, 0.3),
            ),
        ),
    )


def test_transfer_map_json_round_trip():
    transfer_map = TransferMap(
        low_mesh="lowFace_geo",
        high_mesh="highFace_geo",
        records=(
            TransferMapRecord(
                high_vertex_id=0,
                low_face_id=128,
                low_vertex_ids=(12, 42, 43),
                barycentric=(0.2, 0.5, 0.3),
            ),
        ),
    )

    assert loads_transfer_map(dumps_transfer_map(transfer_map)) == transfer_map
