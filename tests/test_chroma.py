"""Chroma key math matches legacy scalar behavior."""

from __future__ import annotations

import math

import numpy as np
import pytest

from greenscreen.chroma import _alpha_from_cb_cr


def _legacy_colorclose(
    cb_p: float, cr_p: float, cb_key: float, cr_key: float, tola: float, tolb: float
) -> float:
    temp = math.sqrt((cb_key - cb_p) ** 2 + (cr_key - cr_p) ** 2)
    if temp < tola:
        z = 0.0
    elif temp < tolb:
        z = (temp - tola) / (tolb - tola)
    else:
        z = 1.0
    return 255.0 * z


@pytest.mark.parametrize(
    ("cb", "cr"),
    [
        (100.0, 130.0),
        (90.0, 120.0),
        (80.0, 110.0),
        (50.0, 50.0),
    ],
)
def test_alpha_matches_legacy(cb: float, cr: float) -> None:
    cb_key, cr_key = 90.0, 120.0
    tola, tolb = 50.0, 130.0
    cb_arr = np.array([[cb]], dtype=np.float64)
    cr_arr = np.array([[cr]], dtype=np.float64)
    got = float(_alpha_from_cb_cr(cb_arr, cr_arr, cb_key, cr_key, tola, tolb)[0, 0])
    exp = _legacy_colorclose(cb, cr, cb_key, cr_key, tola, tolb)
    # Vectorized path returns uint8; legacy reference is float.
    assert abs(got - exp) <= 1.0
