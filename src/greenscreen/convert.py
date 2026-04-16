"""End-to-end: video source to frame folder to alpha PNG folder; optional project layout."""

from __future__ import annotations

import shutil
from pathlib import Path

from rich.console import Console
from yt_dlp.utils import sanitize_filename

from greenscreen.chroma import remove_green_dir
from greenscreen.download import download_audio, download_video, video_title
from greenscreen.frames import extract_frames

console = Console(stderr=True)


def _is_probably_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def run_convert(
    source: str,
    *,
    organize_project: bool = True,
    prefer_ffmpeg: bool = True,
    show_progress: bool = True,
    log: bool = True,
) -> tuple[Path, Path]:
    """
    Download (if URL) or use local video, extract frames, chroma to *_alpha*.

    Returns (frames_dir, alpha_dir).
    """
    cwd = Path(".").resolve()
    apath: Path | None = None
    if _is_probably_url(source):
        if log:
            console.print("[bold green]Source[/bold green]: URL")
        vpath = download_video(source, log=log)
        apath = download_audio(source, log=log)
        label = sanitize_filename(video_title(source), restricted=True)
    else:
        vpath = Path(source).expanduser().resolve()
        if not vpath.is_file():
            raise FileNotFoundError(f"Video not found: {vpath}")
        if log:
            console.print(f"[bold green]Source[/bold green]: local [cyan]{vpath}[/cyan]")
        label = sanitize_filename(vpath.stem, restricted=True)

    frames_dir = extract_frames(
        vpath, prefer_ffmpeg=prefer_ffmpeg, show_progress=show_progress, log=log
    )
    alpha_dir = remove_green_dir(frames_dir, show_progress=show_progress)

    if organize_project:
        project_dir = cwd / f"project_{label}"
        project_dir.mkdir(parents=True, exist_ok=True)
        for p in list(cwd.iterdir()):
            if p == project_dir:
                continue
            if p.is_dir() or p.is_file():
                name = p.name
                if name.startswith(label):
                    dest = project_dir / name
                    if not dest.exists():
                        shutil.move(str(p), str(dest))
        if apath and apath.is_file() and apath.parent == cwd:
            dest = project_dir / apath.name
            if not dest.exists():
                shutil.move(str(apath), str(dest))
        if log:
            console.print(f"[dim]Organized matching files into[/dim] [bold]{project_dir}[/bold]")

    return frames_dir, alpha_dir
