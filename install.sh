#!/usr/bin/env bash
set -e

echo "[1/4] Checking uv..."
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[2/4] Installing Python 3.11..."
uv python install 3.11

echo "[3/4] Creating environment and installing dependencies..."
uv sync

echo "[4/4] Done."
echo ""
echo "Run the application with:"
echo "  uv run dpulse"
