"""APNG + APNGLib (default) or ffmpeg palette (fast) transparent GIF."""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpngw
import numpy as np
from PIL import Image
from rich.console import Console
from tqdm import tqdm

from greenscreen.ffmpeg_util import ffmpeg_executable

console = Console(stderr=True)


def _list_pngs(directory: Path) -> list[Path]:
    return sorted(p for p in directory.iterdir() if p.suffix.lower() == ".png")


def create_gif_apnglib(
    directory: str | Path,
    *,
    delay_ms: int = 50,
    show_progress: bool = True,
) -> Path:
    try:
        import APNGLib  # noqa: PLC0415 — built extension
    except ImportError as e:
        raise RuntimeError(
            "APNGLib extension is not installed (needs libpng + zlib at build time), "
            "or build with SKIP_APNGLIB unset after installing dev libraries. "
            "You can still use `greenscreen gif --fast-ffmpeg` without APNGLib."
        ) from e

    d = Path(directory)
    if not d.is_dir():
        raise FileNotFoundError(f"Not a directory: {d}")
    images_name = _list_pngs(d)
    if not images_name:
        raise FileNotFoundError(f"No PNG files in {d}")

    all_images: list[np.ndarray] = []
    for filename in tqdm(images_name, desc="Load frames", unit="frame", disable=not show_progress):
        all_images.append(np.asarray(Image.open(filename).convert("RGBA")))

    intermediate = d.parent / f"{d.name}_apng_intermediate.apng"
    numpngw.write_apng(str(intermediate), all_images, delay=delay_ms)

    out_gif = d.parent / f"{d.name}.gif"
    APNGLib.MakeGIF(str(intermediate), str(out_gif), 0)
    intermediate.unlink(missing_ok=True)
    console.print(f"[green]GIF[/green] -> [bold]{out_gif}[/bold] (APNGLib path)")
    return out_gif


def create_gif_ffmpeg(
    directory: str | Path,
    *,
    fps: float = 20.0,
    log: bool = True,
) -> Path:
    ffmpeg = ffmpeg_executable()
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH (required for --fast-ffmpeg)")

    d = Path(directory).resolve()
    if not d.is_dir():
        raise FileNotFoundError(f"Not a directory: {d}")
    out_gif = d.parent / f"{d.name}.gif"
    pattern = (d / "%d.png").as_posix()
    vf = (
        f"fps={fps},"
        "split[s0][s1];"
        "[s0]palettegen=max_colors=256:reserve_transparent=1[p];"
        "[s1][p]paletteuse=alpha_threshold=128"
    )
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
        "-vf",
        vf,
        str(out_gif),
    ]
    if log:
        console.print("[cyan]ffmpeg[/cyan] fast GIF (palette, alpha)")
    subprocess.run(cmd, check=True)
    console.print(f"[green]GIF[/green] -> [bold]{out_gif}[/bold] (ffmpeg)")
    return out_gif


def create_gif(
    directory: str | Path,
    *,
    fast_ffmpeg: bool = False,
    delay_ms: int = 50,
    fps: float = 20.0,
    show_progress: bool = True,
) -> Path:
    if fast_ffmpeg:
        return create_gif_ffmpeg(directory, fps=fps)
    return create_gif_apnglib(directory, delay_ms=delay_ms, show_progress=show_progress)
