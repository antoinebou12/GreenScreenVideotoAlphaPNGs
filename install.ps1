#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Install uv: https://docs.astral.sh/uv/getting-started/installation/" -ForegroundColor Yellow
    exit 1
}

# Skip native APNGLib when libpng is not installed (GIF still works with --fast-ffmpeg)
$env:SKIP_APNGLIB = if ($env:SKIP_APNGLIB) { $env:SKIP_APNGLIB } else { "1" }

uv sync --extra dev
Write-Host "Done. Run: uv run greenscreen --help" -ForegroundColor Green
Write-Host "To build APNGLib: install libpng+zlib, then: `$env:SKIP_APNGLIB='0'; uv sync" -ForegroundColor DarkGray
