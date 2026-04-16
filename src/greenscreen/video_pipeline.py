"""Encode RGBA PNG sequence to a video with alpha (ffmpeg)."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console

from greenscreen.ffmpeg_util import ffmpeg_executable

console = Console(stderr=True)


def create_alpha_video(
    directory: str | Path,
    *,
    fps: float = 30.0,
    codec: str = "qtrle",
    log: bool = True,
) -> Path:
    """
    Build ``.mov`` from numbered PNGs (0.png, 1.png, ...) with alpha.

    Default *codec* is ``qtrle`` (QuickTime Animation RGBA); widely supported for transparency.
    Alternative: ``prores_ks`` with ``-profile:v 4444`` if ffmpeg build supports it.
    """
    ffmpeg = ffmpeg_executable()
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")

    d = Path(directory).resolve()
    if not d.is_dir():
        raise FileNotFoundError(f"Not a directory: {d}")

    stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    out = d.parent / f"Videogen-{stamp}.mov"
    pattern = (d / "%d.png").as_posix()

    if codec == "qtrle":
        cmd = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            pattern,
            "-c:v",
            "qtrle",
            str(out),
        ]
    elif codec == "prores_4444":
        cmd = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            pattern,
            "-c:v",
            "prores_ks",
            "-profile:v",
            "4444",
            "-pix_fmt",
            "yuva444p10le",
            str(out),
        ]
    else:
        raise ValueError(f"Unknown codec preset: {codec}")

    if log:
        console.print(f"[cyan]ffmpeg[/cyan] alpha video [dim]{codec}[/dim] @ {fps} fps")
    subprocess.run(cmd, check=True)
    console.print(f"[green]Video[/green] -> [bold]{out}[/bold]")
    return out
