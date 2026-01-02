@echo off
REM DaVinci Resolve MCP Server - Windows Entry Point
REM Usage: resolve-mcp.bat

setlocal

set "SCRIPT_DIR=%~dp0"
set "RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
set "RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
set "PYTHONPATH=%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules"

REM Check if venv exists
if exist "%SCRIPT_DIR%venv\Scripts\python.exe" (
    "%SCRIPT_DIR%venv\Scripts\python.exe" -m src
) else (
    python "%SCRIPT_DIR%src\__main__.py"
)
