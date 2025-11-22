#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip build
python -m build

echo "Artifacts written to dist/. Tag and upload as needed."
