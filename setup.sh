#!/usr/bin/env bash
# Setup script for scrollytelling-generator skill
# Run from the skill directory: ./setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/scripts/.venv"

echo "Setting up scrollytelling-generator..."

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "Error: Python 3 is required. Install it and re-run."
  exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PY_VERSION"

# Create venv and install python-pptx
if [ -d "$VENV_DIR" ]; then
  echo "Venv already exists at scripts/.venv/"
else
  echo "Creating venv at scripts/.venv/..."
  python3 -m venv "$VENV_DIR"
  "$VENV_DIR/bin/pip" install --quiet python-pptx
  echo "Installed python-pptx"
fi

# Check LibreOffice
if command -v libreoffice &>/dev/null || [ -d "/Applications/LibreOffice.app" ]; then
  echo "Found LibreOffice"
else
  echo ""
  echo "Warning: LibreOffice not found."
  echo "  macOS:  brew install --cask libreoffice"
  echo "  Linux:  sudo apt install libreoffice"
  echo ""
  echo "LibreOffice is required for slide image export."
fi

echo ""
echo "Setup complete. Install location: $SCRIPT_DIR"
