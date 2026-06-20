import pytest

from icarus_dcc.uv_delta_transfer.records import TransferMap, TransferMapRecord


def test_transfer_map_record_normalizes_values():
    record = TransferMapRecord(
        high_vertex_id=4,
        low_face_id=12,
        low_vertex_ids=(1, 2, 3),
        barycentric=(0, 0.25, 0.75),
    )

    assert record.high_vertex_id == 4
    assert record.low_face_id == 12
    assert record.low_vertex_ids == (1, 2, 3)
    assert record.barycentric == (0.0, 0.25, 0.75)


def test_transfer_map_record_rejects_invalid_ids():
    with pytest.raises(ValueError):
        TransferMapRecord(
            high_vertex_id=-1,
            low_face_id=12,
            low_vertex_ids=(1, 2, 3),
            barycentric=(0.0, 0.25, 0.75),
        )


def test_transfer_map_record_rejects_invalid_triplet_lengths():
    with pytest.raises(ValueError):
        TransferMapRecord(
            high_vertex_id=4,
            low_face_id=12,
            low_vertex_ids=(1, 2),
            barycentric=(0.0, 0.25, 0.75),
        )


def test_transfer_map_record_validates_barycentric_sum():
    record = TransferMapRecord(
        high_vertex_id=4,
        low_face_id=12,
        low_vertex_ids=(1, 2, 3),
        barycentric=(0.25, 0.25, 0.25),
    )

    with pytest.raises(ValueError):
        record.validate_barycentric_sum()


def test_transfer_map_defaults_to_map1():
    transfer_map = TransferMap(low_mesh="lowFace_geo", high_mesh="highFace_geo")

    assert transfer_map.uv_set == "map1"
    assert transfer_map.records == ()


def test_transfer_map_validates_record_count():
    transfer_map = TransferMap(
        low_mesh="lowFace_geo",
        high_mesh="highFace_geo",
        records=(
            TransferMapRecord(
                high_vertex_id=0,
                low_face_id=12,
                low_vertex_ids=(1, 2, 3),
                barycentric=(0.5, 0.25, 0.25),
            ),
        ),
    )

    transfer_map.validate_record_count(high_vertex_count=1)

    with pytest.raises(ValueError):
        transfer_map.validate_record_count(high_vertex_count=2)


def test_transfer_map_validates_all_barycentric_weights():
    transfer_map = TransferMap(
        low_mesh="lowFace_geo",
        high_mesh="highFace_geo",
        records=(
            TransferMapRecord(
                high_vertex_id=0,
                low_face_id=12,
                low_vertex_ids=(1, 2, 3),
                barycentric=(0.5, 0.25, 0.25),
            ),
            TransferMapRecord(
                high_vertex_id=1,
                low_face_id=13,
                low_vertex_ids=(4, 5, 6),
                barycentric=(0.25, 0.25, 0.25),
            ),
        ),
    )

    with pytest.raises(ValueError):
        transfer_map.validate_barycentric_weights()
