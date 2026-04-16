#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Prefer uv (modern). Legacy youtube-dl install removed in favor of yt-dlp (PyPI).
if command -v uv >/dev/null 2>&1; then
  export SKIP_APNGLIB="${SKIP_APNGLIB:-1}"
  uv sync --extra dev
  echo "Done. Run: uv run greenscreen --help"
  echo "To build APNGLib: install libpng-dev zlib1g-dev, then: SKIP_APNGLIB=0 uv sync"
  exit 0
fi

echo "Install uv: https://docs.astral.sh/uv/getting-started/installation/"
echo "Falling back to pip (set SKIP_APNGLIB=0 to attempt APNGLib build)..."
export SKIP_APNGLIB="${SKIP_APNGLIB:-1}"
pip3 install -e ".[dev]"
