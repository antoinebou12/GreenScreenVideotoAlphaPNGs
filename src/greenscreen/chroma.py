"""Vectorized YCbCr chroma key to RGBA PNG (same math as legacy colorclose)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageChops
from tqdm import tqdm


def _alpha_from_cb_cr(
    cb: np.ndarray,
    cr: np.ndarray,
    cb_key: float,
    cr_key: float,
    tola: float,
    tolb: float,
) -> np.ndarray:
    """Return uint8 alpha 0–255: 0 = keyed (transparent), 255 = opaque."""
    temp = np.sqrt(((cb_key - cb) ** 2 + (cr_key - cr) ** 2).astype(np.float64))
    z = np.zeros_like(temp, dtype=np.float64)
    z[temp >= tolb] = 1.0
    mid = (temp >= tola) & (temp < tolb)
    z[mid] = (temp[mid] - tola) / (tolb - tola)
    return (255.0 * z).astype(np.uint8)


def green_screen_rgba(
    infile: str | Path,
    outfile: str | Path,
    *,
    key_color: tuple[int, int, int] | None = None,
    tolerance: tuple[float, float] | None = None,
) -> None:
    """Replace green screen with alpha using YCbCr distance (vectorized)."""
    in_path = Path(infile)
    out_path = Path(outfile)
    in_data = Image.open(in_path).convert("YCbCr")
    if key_color is None:
        key_color = in_data.getpixel((1, 1))
    if tolerance is None:
        tolerance = (50.0, 130.0)
    _y_key, cb_key, cr_key = key_color
    tola, tolb = tolerance

    w, h = in_data.size
    arr = np.asarray(in_data, dtype=np.uint8)  # (H, W, 3)
    cb = arr[:, :, 1].astype(np.float64)
    cr = arr[:, :, 2].astype(np.float64)

    alpha_mask = _alpha_from_cb_cr(cb, cr, float(cb_key), float(cr_key), tola, tolb)
    invert_mask = Image.fromarray(np.uint8(255 - alpha_mask), mode="L")

    color_mask = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    all_green = Image.new("YCbCr", (w, h), tuple(key_color))
    color_mask.paste(all_green, invert_mask)

    rgba = in_data.convert("RGBA")
    cleaned = ImageChops.subtract(rgba, color_mask)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.save(out_path, "PNG")


def remove_green_dir(
    directory: str | Path,
    *,
    show_progress: bool = True,
) -> Path:
    """Process all *.png in *directory*; write *_alpha* sibling folder."""
    d = Path(directory)
    if not d.is_dir():
        raise FileNotFoundError(f"Not a directory: {d}")
    images = sorted([p for p in d.iterdir() if p.suffix.lower() == ".png"])
    out_dir = Path(f"{d}_alpha")
    out_dir.mkdir(parents=True, exist_ok=True)
    it = tqdm(images, desc="Chroma key", unit="frame", disable=not show_progress)
    for p in it:
        green_screen_rgba(p, out_dir / p.name)
    return out_dir
