"""Typer CLI: convert | gif | video."""

from __future__ import annotations

import typer
from rich.console import Console

from greenscreen.convert import run_convert
from greenscreen.gif_pipeline import create_gif
from greenscreen.video_pipeline import create_alpha_video

rich_console = Console(stderr=True)
app = typer.Typer(
    name="greenscreen",
    help="Green screen video to alpha PNG sequences, GIF, and transparent video.",
    no_args_is_help=True,
)


@app.command("convert")
def cmd_convert(
    source: str = typer.Argument(..., help="YouTube URL or path to a video file"),
    no_project_dir: bool = typer.Option(
        False,
        "--no-project-dir",
        help="Do not move outputs into project_<title>/",
    ),
    no_ffmpeg: bool = typer.Option(
        False,
        "--no-ffmpeg",
        help="Force OpenCV frame extraction instead of ffmpeg",
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Less console output"),
) -> None:
    """Download (or use local video), extract frames, apply chroma key."""
    run_convert(
        source,
        organize_project=not no_project_dir,
        prefer_ffmpeg=not no_ffmpeg,
        show_progress=not quiet,
        log=not quiet,
    )
    if not quiet:
        rich_console.print("[bold green]Done.[/bold green]")


@app.command("gif")
def cmd_gif(
    directory: str = typer.Argument(..., help="Folder of RGBA PNG frames (e.g. *_alpha)"),
    fast_ffmpeg: bool = typer.Option(
        False,
        "--fast-ffmpeg",
        help="Use ffmpeg palette (faster); default uses numpngw + APNGLib",
    ),
    delay_ms: int = typer.Option(50, "--delay-ms", help="Frame delay for APNG path (ms)"),
    fps: float = typer.Option(20.0, "--fps", help="FPS for --fast-ffmpeg"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
) -> None:
    """Build a transparent GIF from a PNG sequence."""
    create_gif(
        directory,
        fast_ffmpeg=fast_ffmpeg,
        delay_ms=delay_ms,
        fps=fps,
        show_progress=not quiet,
    )
    if not quiet:
        rich_console.print("[bold green]Done.[/bold green]")


@app.command("video")
def cmd_video(
    directory: str = typer.Argument(..., help="Folder of RGBA PNG frames (e.g. *_alpha)"),
    fps: float = typer.Option(30.0, "--fps", help="Output frame rate"),
    codec: str = typer.Option(
        "qtrle",
        "--codec",
        help="qtrle (default, alpha) or prores_4444 (if ffmpeg supports it)",
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
) -> None:
    """Encode PNG sequence to a QuickTime-compatible video with alpha."""
    if codec not in ("qtrle", "prores_4444"):
        raise typer.BadParameter("codec must be qtrle or prores_4444")
    create_alpha_video(directory, fps=fps, codec=codec, log=not quiet)
    if not quiet:
        rich_console.print("[bold green]Done.[/bold green]")
