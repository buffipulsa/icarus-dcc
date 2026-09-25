import pytest

from icarus_dcc.uv_delta_transfer.uv_math import (
    DegenerateTriangleError,
    barycentric_from_uv,
    is_point_inside_triangle,
)


def test_barycentric_from_uv_returns_vertex_weights():
    weights = barycentric_from_uv(
        point_uv=(0.0, 0.0),
        tri_uv_a=(0.0, 0.0),
        tri_uv_b=(1.0, 0.0),
        tri_uv_c=(0.0, 1.0),
    )

    assert weights == pytest.approx((1.0, 0.0, 0.0))


def test_barycentric_from_uv_returns_interior_weights():
    weights = barycentric_from_uv(
        point_uv=(0.25, 0.25),
        tri_uv_a=(0.0, 0.0),
        tri_uv_b=(1.0, 0.0),
        tri_uv_c=(0.0, 1.0),
    )

    assert weights == pytest.approx((0.5, 0.25, 0.25))


def test_barycentric_from_uv_returns_edge_weights():
    weights = barycentric_from_uv(
        point_uv=(0.5, 0.5),
        tri_uv_a=(0.0, 0.0),
        tri_uv_b=(1.0, 0.0),
        tri_uv_c=(0.0, 1.0),
    )

    assert weights == pytest.approx((0.0, 0.5, 0.5))


def test_barycentric_from_uv_supports_outside_points():
    weights = barycentric_from_uv(
        point_uv=(1.25, 0.25),
        tri_uv_a=(0.0, 0.0),
        tri_uv_b=(1.0, 0.0),
        tri_uv_c=(0.0, 1.0),
    )

    assert weights == pytest.approx((-0.5, 1.25, 0.25))


def test_barycentric_from_uv_rejects_degenerate_triangle():
    with pytest.raises(DegenerateTriangleError):
        barycentric_from_uv(
            point_uv=(0.25, 0.25),
            tri_uv_a=(0.0, 0.0),
            tri_uv_b=(1.0, 1.0),
            tri_uv_c=(2.0, 2.0),
        )


def test_is_point_inside_triangle_accepts_interior_and_edges():
    assert is_point_inside_triangle((0.5, 0.25, 0.25))
    assert is_point_inside_triangle((0.0, 0.5, 0.5))


def test_is_point_inside_triangle_allows_small_border_tolerance():
    assert is_point_inside_triangle((-0.000001, 0.500001, 0.5), tolerance=1e-5)


def test_is_point_inside_triangle_rejects_outside_weights():
    assert not is_point_inside_triangle((-0.1, 0.6, 0.5))


def test_is_point_inside_triangle_rejects_weights_that_do_not_sum_to_one():
    assert not is_point_inside_triangle((0.25, 0.25, 0.25))


def test_uv_inputs_must_be_two_values():
    with pytest.raises(ValueError):
        barycentric_from_uv(
            point_uv=(0.25, 0.25, 0.0),
            tri_uv_a=(0.0, 0.0),
            tri_uv_b=(1.0, 0.0),
            tri_uv_c=(0.0, 1.0),
        )


def test_barycentric_weights_must_be_three_values():
    with pytest.raises(ValueError):
        is_point_inside_triangle((0.5, 0.5))
