"""Extract video frames to PNG sequence (ffmpeg preferred, OpenCV fallback)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import cv2
from tqdm import tqdm

from greenscreen.ffmpeg_util import ffmpeg_executable


def extract_frames_ffmpeg(video: Path, out_dir: Path, *, log: bool = True) -> int:
    ffmpeg = ffmpeg_executable()
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(out_dir / "%d.png")
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(video),
        "-vsync",
        "0",
        "-y",
        pattern,
    ]
    if log:
        print("Using ffmpeg for frame extraction", file=sys.stderr)
    subprocess.run(cmd, check=True)
    frames = sorted(out_dir.glob("*.png"))
    return len(frames)


def extract_frames_opencv(video: Path, out_dir: Path, *, show_progress: bool = True) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise OSError(f"Could not open video: {video}")
    count = 0
    pbar = tqdm(desc="Frames (OpenCV)", unit="frame", disable=not show_progress)
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imwrite(str(out_dir / f"{count}.png"), frame)
        count += 1
        pbar.update(1)
    pbar.close()
    cap.release()
    return count


def extract_frames(
    video: Path,
    out_dir: Path | None = None,
    *,
    prefer_ffmpeg: bool = True,
    show_progress: bool = True,
    log: bool = True,
) -> Path:
    """Write numbered PNGs (0.png, 1.png, ...) into ``video.stem`` folder (or *out_dir*)."""
    if out_dir is None:
        out_dir = video.parent / video.stem
    out_dir = Path(out_dir)
    if prefer_ffmpeg and ffmpeg_executable():
        n = extract_frames_ffmpeg(video, out_dir, log=log)
        if log:
            print(f"Extracted {n} frames -> {out_dir}", file=sys.stderr)
        return out_dir
    if log:
        print("ffmpeg not found; using OpenCV (slower)", file=sys.stderr)
    extract_frames_opencv(video, out_dir, show_progress=show_progress)
    return out_dir
