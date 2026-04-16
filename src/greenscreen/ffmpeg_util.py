"""Resolve ffmpeg binary: PATH first, then imageio-ffmpeg bundled binary."""

from __future__ import annotations

import shutil


def ffmpeg_executable() -> str | None:
    path = shutil.which("ffmpeg")
    if path:
        return path
    try:
        import imageio_ffmpeg  # type: ignore[import-untyped]

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None
