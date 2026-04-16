#!/usr/bin/env python3
"""Legacy shim: use ``greenscreen video`` (Typer CLI)."""

from __future__ import annotations

import sys

from greenscreen.cli import app


def main() -> None:
    # Map legacy --fps to Typer (Typer uses same flag name on subcommand)
    sys.argv = ["greenscreen", "video", *sys.argv[1:]]
    app()


if __name__ == "__main__":
    main()
