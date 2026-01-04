#!/usr/bin/env bash
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

echo "Syncing packages..."
uv sync

echo "Starting UpBack on port $PORT..."
uv run upback --port "$PORT"
