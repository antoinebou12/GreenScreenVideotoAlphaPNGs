#!/usr/bin/env python3
"""Legacy shim: use ``greenscreen convert`` (Typer CLI)."""

from __future__ import annotations

import sys

from greenscreen.cli import app


def main() -> None:
    sys.argv = ["greenscreen", "convert", *sys.argv[1:]]
    app()


if __name__ == "__main__":
    main()
