@echo off
REM DaVinci Resolve MCP Server - Pre-Launch Check for Windows
REM This batch file launches the PowerShell pre-launch check script

echo Starting DaVinci Resolve MCP Pre-Launch Check...
echo.

REM Run the PowerShell script with bypass execution policy for this session only
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\check-resolve-ready.ps1"

echo.
if %ERRORLEVEL% EQU 0 (
    echo Pre-launch check completed successfully.
) else (
    echo Pre-launch check encountered issues. Please review any error messages above.
    pause
) 