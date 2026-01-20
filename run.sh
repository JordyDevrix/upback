#!/usr/bin/env bash
set -e
# run.sh - cross-platform script to sync and run UpBack


# Default port
PORT=8080

# Allow passing --port=XXXX or -p XXXX
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --port) PORT="$2"; shift ;;
        -p) PORT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


# Build frontend
echo "Building Vue frontend..."
cd src/frontend/upback-frontend
npm install
npm run build

# Go back to root folder
cd ../../..

ls

echo "Activating virtual environment..."
# macOS / Linux activation
if [[ "$(uname)" == "Darwin" || "$(uname)" == "Linux" ]]; then
    source .venv/bin/activate
else
    echo "Unsupported OS for this script."
    exit 1
fi

echo "Syncing packages..."
uv sync

# Starting UpBack service
echo "Starting UpBack on port $PORT..."
uv run upback --port "$PORT"
