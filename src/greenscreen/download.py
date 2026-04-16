"""yt-dlp wrappers with Rich logging."""

from __future__ import annotations

from pathlib import Path

import yt_dlp
from rich.console import Console

console = Console(stderr=True)


def video_title(url: str) -> str:
    with yt_dlp.YoutubeDL(
        {"quiet": True, "no_warnings": True, "simulate": True, "skip_download": True}
    ) as ydl:
        info = ydl.extract_info(url, download=False)
        assert info is not None
        return str(info["title"])


def download_video(url: str, *, log: bool = True) -> Path:
    last: dict = {}

    def _hook(d: dict) -> None:
        nonlocal last
        if d.get("status") == "finished":
            last = d

    opts: dict = {
        "format": "mp4/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": "%(title)s.%(ext)s",
        "no_warnings": True,
        "quiet": not log,
        "progress_hooks": [_hook],
    }
    if log:
        console.print("[cyan]Downloading video...[/cyan]")
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    if last.get("filename"):
        return Path(str(last["filename"])).resolve()
    # Fallback: newest mp4 in cwd (single-download sessions)
    mp4s = sorted(Path(".").glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
    if mp4s:
        return mp4s[0].resolve()
    raise FileNotFoundError("Download finished but output mp4 path could not be resolved")


def download_audio(url: str, *, log: bool = True) -> Path:
    last: dict = {}

    def _hook(d: dict) -> None:
        nonlocal last
        if d.get("status") == "finished":
            last = d

    opts: dict = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "no_warnings": True,
        "quiet": not log,
        "progress_hooks": [_hook],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    if log:
        console.print("[cyan]Downloading audio...[/cyan]")
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    if last.get("filename"):
        return Path(str(last["filename"])).resolve()
    mp3s = sorted(Path(".").glob("*.mp3"), key=lambda p: p.stat().st_mtime, reverse=True)
    if mp3s:
        return mp3s[0].resolve()
    raise FileNotFoundError("Download finished but output mp3 path could not be resolved")
