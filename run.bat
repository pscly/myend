@echo off
cd /d %~dp0\flask_s
uv sync && uv run python app.py
