:: run.bat
@echo off
set PORT=8080
if not "%1"=="" set PORT=%1

uv sync
uv run upback --port %PORT%
