"""Build APNGLib C++ extension alongside the greenscreen package (setuptools + PEP 621)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from setuptools import Extension, setup

ROOT = Path(__file__).resolve().parent
APNG_SRC = str(ROOT / "lib" / "APNGLib_fix" / "APNGLib" / "APNGLib.cpp")


def _extension_libraries() -> list[str]:
    # MSYS2 / vcpkg / conda vary; override with LDFLAGS / LIBRARY_PATH if needed.
    if sys.platform == "win32":
        return ["png", "z"]
    return ["stdc++", "m", "png", "z"]


def _ext_modules() -> list[Extension]:
    if os.environ.get("SKIP_APNGLIB", "").lower() in ("1", "true", "yes"):
        print(
            "SKIP_APNGLIB set: building without APNGLib (use --fast-ffmpeg for GIF).",
            file=sys.stderr,
        )
        return []
    return [
        Extension(
            name="APNGLib",
            sources=[APNG_SRC],
            libraries=_extension_libraries(),
            language="c++",
            extra_compile_args=["/std:c++17"] if sys.platform == "win32" else ["-std=c++17"],
        )
    ]


setup(ext_modules=_ext_modules())
