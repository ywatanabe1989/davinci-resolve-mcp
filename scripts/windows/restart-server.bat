@echo off
:: Restart script for DaVinci Resolve MCP Server
:: Created as part of feature updates on March 29, 2024

echo ========================================================
echo DaVinci Resolve MCP Server - Restart Script
echo ========================================================

:: Change to the directory where the script is located
cd /d "%~dp0"

:: Check if the server is running
echo Checking for running server...
wmic process where "commandline like '%%python%%src\__main__.py%%'" get processid 2>nul | findstr /r "[0-9]" > temp_pid.txt

:: Check if any PID was found
set /p SERVER_PID=<temp_pid.txt
del temp_pid.txt

if not defined SERVER_PID (
    echo No running DaVinci Resolve MCP Server detected.
) else (
    echo Stopping existing DaVinci Resolve MCP Server with PID: %SERVER_PID%
    
    :: Stop the process
    taskkill /PID %SERVER_PID% /F
    
    :: Wait a moment to ensure it's stopped
    timeout /t 2 /nobreak > nul
    
    echo Server process stopped.
)

:: Make sure we have the right environment
if exist setup.bat (
    echo Setting up environment...
    call setup.bat
) else (
    echo Warning: setup.bat not found. Environment may not be properly configured.
)

:: Start the server again
echo Starting DaVinci Resolve MCP Server...
if exist "%SCRIPT_DIR%\..\run-now.bat" (
    echo Starting server with run-now.bat...
    start "" cmd /c "%SCRIPT_DIR%\..\run-now.bat"
    
    :: Wait a moment
    timeout /t 3 /nobreak > nul
    
    :: Check if it started
    wmic process where "commandline like '%%python%%src\__main__.py%%'" get processid 2>nul | findstr /r "[0-9]" > nul
    if %ERRORLEVEL% EQU 0 (
        echo DaVinci Resolve MCP Server started successfully!
    ) else (
        echo Failed to start DaVinci Resolve MCP Server. Check logs for errors.
    )
) else (
    echo Error: run-now.bat not found. Cannot start the server.
    exit /b 1
)

echo ========================================================
echo Restart operation completed.
echo ======================================================== 