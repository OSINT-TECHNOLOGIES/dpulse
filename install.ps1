Write-Host "[1/4] Checking uv..."
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "uv not found. Installing uv..."
    irm https://astral.sh/uv/install.ps1 | iex
}

Write-Host "[2/4] Installing Python 3.11..."
uv python install 3.11

Write-Host "[3/4] Creating environment and installing dependencies..."
uv sync

Write-Host "[4/4] Done."
Write-Host ""
Write-Host "Run the application with:"
Write-Host "  uv run dpulse"
