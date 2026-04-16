"""
APNGLib is built from the repository root (setuptools + pyproject.toml + setup.py).

Install the project in editable mode from the repo root::

    uv sync --extra dev
    # or: pip install -e ".[dev]"

This file is kept only for backwards compatibility; it forwards to setuptools.
"""

from __future__ import annotations

import sys
from pathlib import Path

from setuptools import Extension, setup

ROOT = Path(__file__).resolve().parents[2]
APNG_SRC = str(ROOT / "lib" / "APNGLib_fix" / "APNGLib" / "APNGLib.cpp")


def _libraries() -> list[str]:
    if sys.platform == "win32":
        return ["png", "z"]
    return ["stdc++", "m", "png", "z"]


if __name__ == "__main__":
    setup(
        name="APNGLib-legacy-local",
        version="1.0",
        ext_modules=[
            Extension(
                "APNGLib",
                sources=[APNG_SRC],
                libraries=_libraries(),
                language="c++",
                extra_compile_args=["/std:c++17"] if sys.platform == "win32" else ["-std=c++17"],
            )
        ],
    )
