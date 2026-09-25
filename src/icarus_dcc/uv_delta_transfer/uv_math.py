"""Pure UV math helpers for UV delta transfer."""

from __future__ import annotations

from collections.abc import Sequence

UV = tuple[float, float]
BarycentricWeights = tuple[float, float, float]


class DegenerateTriangleError(ValueError):
    """Raised when barycentric weights are requested for a zero-area triangle."""


def _as_uv(value: Sequence[float], name: str) -> UV:
    if len(value) != 2:
        msg = f"{name} must contain exactly two values."
        raise ValueError(msg)

    return (float(value[0]), float(value[1]))


def barycentric_from_uv(
    point_uv: Sequence[float],
    tri_uv_a: Sequence[float],
    tri_uv_b: Sequence[float],
    tri_uv_c: Sequence[float],
    *,
    epsilon: float = 1e-12,
) -> BarycentricWeights:
    """Return barycentric weights for a point in UV triangle space.

    The returned weights correspond to ``tri_uv_a``, ``tri_uv_b``, and ``tri_uv_c``.
    Points outside the triangle still produce weights, which lets callers decide how
    much tolerance to allow when testing containment.

    Parameters
    ----------
    point_uv
        UV coordinate to evaluate.
    tri_uv_a
        First triangle UV coordinate.
    tri_uv_b
        Second triangle UV coordinate.
    tri_uv_c
        Third triangle UV coordinate.
    epsilon
        Minimum absolute triangle area denominator before the triangle is treated as
        degenerate.

    Returns
    -------
    tuple[float, float, float]
        Barycentric weights for ``tri_uv_a``, ``tri_uv_b``, and ``tri_uv_c``.

    Raises
    ------
    ValueError
        If any UV input does not contain exactly two values.
    DegenerateTriangleError
        If the triangle has no usable UV area.
    """

    point = _as_uv(point_uv, "point_uv")
    uv_a = _as_uv(tri_uv_a, "tri_uv_a")
    uv_b = _as_uv(tri_uv_b, "tri_uv_b")
    uv_c = _as_uv(tri_uv_c, "tri_uv_c")

    vector_ab = (uv_b[0] - uv_a[0], uv_b[1] - uv_a[1])
    vector_ac = (uv_c[0] - uv_a[0], uv_c[1] - uv_a[1])
    vector_ap = (point[0] - uv_a[0], point[1] - uv_a[1])

    denominator = vector_ab[0] * vector_ac[1] - vector_ac[0] * vector_ab[1]
    if abs(denominator) <= epsilon:
        msg = "Cannot calculate barycentric weights for a degenerate UV triangle."
        raise DegenerateTriangleError(msg)

    weight_b = (vector_ap[0] * vector_ac[1] - vector_ac[0] * vector_ap[1]) / denominator
    weight_c = (vector_ab[0] * vector_ap[1] - vector_ap[0] * vector_ab[1]) / denominator
    weight_a = 1.0 - weight_b - weight_c

    return (weight_a, weight_b, weight_c)


def is_point_inside_triangle(
    weights: Sequence[float],
    tolerance: float = 1e-5,
) -> bool:
    """Return True if barycentric weights describe a point inside a triangle.

    Parameters
    ----------
    weights
        Three barycentric weights to test.
    tolerance
        Allowed negative border tolerance and allowed deviation from a weight sum of
        ``1.0``.

    Returns
    -------
    bool
        ``True`` when all weights are inside the triangle within tolerance.

    Raises
    ------
    ValueError
        If ``weights`` does not contain exactly three values.
    """

    if len(weights) != 3:
        msg = "weights must contain exactly three values."
        raise ValueError(msg)

    barycentric = (float(weights[0]), float(weights[1]), float(weights[2]))
    weight_sum = barycentric[0] + barycentric[1] + barycentric[2]

    return (
        abs(weight_sum - 1.0) <= tolerance
        and barycentric[0] >= -tolerance
        and barycentric[1] >= -tolerance
        and barycentric[2] >= -tolerance
    )

