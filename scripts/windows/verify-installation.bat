@echo off
REM verify-installation.bat
REM Script to verify that the DaVinci Resolve MCP installation has been properly set up

title DaVinci Resolve MCP Installation Verification

REM Colors for terminal output
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set RED=[91m
set NC=[0m

REM Get the script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "VENV_DIR=%PROJECT_ROOT%\venv"

echo %BLUE%===============================================%NC%
echo %BLUE%  DaVinci Resolve MCP Installation Verification  %NC%
echo %BLUE%===============================================%NC%

REM Check if virtual environment exists
echo %YELLOW%Checking Python virtual environment... %NC%
if exist "%VENV_DIR%\Scripts\python.exe" (
    echo %GREEN%OK%NC%
    set /a "venv_check=1"
) else (
    echo %RED%MISSING%NC%
    echo %RED%Virtual environment not found at: %VENV_DIR%%NC%
    set /a "venv_check=0"
)

REM Check if MCP SDK is installed
echo %YELLOW%Checking MCP SDK installation... %NC%
"%VENV_DIR%\Scripts\pip" list | findstr "mcp" > nul
if %ERRORLEVEL% == 0 (
    echo %GREEN%OK%NC%
    set /a "mcp_check=1"
) else (
    echo %RED%MISSING%NC%
    echo %RED%MCP SDK not installed in the virtual environment%NC%
    set /a "mcp_check=0"
)

REM Check if Resolve MCP server script exists
echo %YELLOW%Checking server script... %NC%
if exist "%PROJECT_ROOT%\src\src\__main__.py" (
    echo %GREEN%OK%NC%
    set /a "script_check=1"
) else (
    echo %RED%MISSING%NC%
    echo %RED%Server script not found at: %PROJECT_ROOT%\src\src\__main__.py%NC%
    set /a "script_check=0"
)

REM Check if DaVinci Resolve is running
echo %YELLOW%Checking if DaVinci Resolve is running... %NC%
tasklist /FI "IMAGENAME eq Resolve.exe" 2>NUL | find /I /N "Resolve.exe">NUL
if %ERRORLEVEL% == 0 (
    echo %GREEN%OK%NC%
    set /a "resolve_check=1"
) else (
    echo %RED%NOT RUNNING%NC%
    echo %RED%DaVinci Resolve is not running - please start it%NC%
    set /a "resolve_check=0"
)

REM Check Cursor MCP configuration
echo %YELLOW%Checking Cursor MCP configuration... %NC%
set "CURSOR_CONFIG_FILE=%APPDATA%\Cursor\mcp\config.json"
if exist "%CURSOR_CONFIG_FILE%" (
    findstr "davinci-resolve" "%CURSOR_CONFIG_FILE%" > nul
    if %ERRORLEVEL% == 0 (
        echo %GREEN%OK%NC%
        echo %GREEN%Cursor MCP config found at: %CURSOR_CONFIG_FILE%%NC%
        set /a "cursor_check=1"
    ) else (
        echo %RED%INVALID%NC%
        echo %RED%Cursor MCP config does not contain 'davinci-resolve' entry%NC%
        set /a "cursor_check=0"
    )
) else (
    echo %RED%MISSING%NC%
    echo %RED%Cursor MCP config not found at: %CURSOR_CONFIG_FILE%%NC%
    set /a "cursor_check=0"
)

REM Check if all environment variables are set
echo %YELLOW%Checking environment variables... %NC%
set /a "env_vars_missing=0"

if "%RESOLVE_SCRIPT_API%"=="" (
    set /a "env_vars_missing=1"
)

if "%RESOLVE_SCRIPT_LIB%"=="" (
    set /a "env_vars_missing=1"
)

if "%PYTHONPATH%"=="" (
    set /a "env_vars_missing=1"
) else (
    echo %PYTHONPATH% | findstr "Modules" > nul
    if %ERRORLEVEL% NEQ 0 (
        set /a "env_vars_missing=1"
    )
)

if %env_vars_missing% == 0 (
    echo %GREEN%OK%NC%
    set /a "env_check=1"
) else (
    echo %RED%MISSING%NC%
    echo %RED%One or more required environment variables are not set%NC%
    set /a "env_check=0"
)

REM Calculate total checks passed
set /a "total_checks=6"
set /a "passed_checks=venv_check+mcp_check+script_check+resolve_check+cursor_check+env_check"

echo %BLUE%=============================================%NC%
echo %YELLOW%Results: %passed_checks%/%total_checks% checks passed%NC%

if %passed_checks% == %total_checks% (
    echo %GREEN%[✓] Installation verification completed successfully!%NC%
    echo %GREEN%[✓] You can now use the MCP server with DaVinci Resolve%NC%
    echo %YELLOW%To start the server, run:%NC%
    echo %BLUE%  run-now.bat%NC%
    echo %YELLOW%Or for more options:%NC%
    echo %BLUE%  scripts\mcp_resolve-cursor_start%NC%
    exit /b 0
) else (
    echo %RED%[✗] Installation verification failed!%NC%
    echo %YELLOW%Please fix the issues above and run this script again%NC%
    exit /b 1
) 