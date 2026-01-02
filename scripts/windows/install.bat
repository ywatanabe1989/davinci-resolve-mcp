@echo off
REM install.bat - One-step installation for DaVinci Resolve MCP Integration
REM This script handles the entire installation process with improved error detection

setlocal EnableDelayedExpansion

REM Colors for terminal output
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set RED=[91m
set BOLD=[1m
set NC=[0m

REM Get the absolute path of this script's location
set "INSTALL_DIR=%~dp0"
set "INSTALL_DIR=%INSTALL_DIR:~0,-1%"
set "VENV_DIR=%INSTALL_DIR%\venv"
set "CURSOR_CONFIG_DIR=%APPDATA%\Cursor\mcp"
set "CURSOR_CONFIG_FILE=%CURSOR_CONFIG_DIR%\config.json"
set "PROJECT_CURSOR_DIR=%INSTALL_DIR%\.cursor"
set "PROJECT_CONFIG_FILE=%PROJECT_CURSOR_DIR%\mcp.json"
set "LOG_FILE=%INSTALL_DIR%\install.log"

REM Banner
echo %BLUE%%BOLD%=================================================%NC%
echo %BLUE%%BOLD%  DaVinci Resolve MCP Integration Installer      %NC%
echo %BLUE%%BOLD%=================================================%NC%
echo %YELLOW%Installation directory: %INSTALL_DIR%%NC%
echo Installation log: %LOG_FILE%
echo.

REM Initialize log
echo === DaVinci Resolve MCP Installation Log === > "%LOG_FILE%"
echo Date: %date% %time% >> "%LOG_FILE%"
echo Install directory: %INSTALL_DIR% >> "%LOG_FILE%"
echo User: %USERNAME% >> "%LOG_FILE%"
echo System: %OS% Windows %PROCESSOR_ARCHITECTURE% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Function to log messages (call :log "Message")
:log
echo [%time%] %~1 >> "%LOG_FILE%"
exit /b 0

REM Check if DaVinci Resolve is running
:check_resolve_running
call :log "Checking if DaVinci Resolve is running"
echo %YELLOW%Checking if DaVinci Resolve is running... %NC%

tasklist /FI "IMAGENAME eq Resolve.exe" 2>NUL | find /I /N "Resolve.exe">NUL
if %ERRORLEVEL% == 0 (
    echo %GREEN%OK%NC%
    call :log "DaVinci Resolve is running"
    set RESOLVE_RUNNING=1
) else (
    echo %RED%NOT RUNNING%NC%
    echo %YELLOW%DaVinci Resolve must be running to complete the installation.%NC%
    echo %YELLOW%Please start DaVinci Resolve and try again.%NC%
    call :log "DaVinci Resolve is not running - installation cannot proceed"
    set RESOLVE_RUNNING=0
)
exit /b %RESOLVE_RUNNING%

REM Create Python virtual environment
:create_venv
call :log "Creating/checking Python virtual environment"
echo %YELLOW%Setting up Python virtual environment... %NC%

if exist "%VENV_DIR%\Scripts\python.exe" (
    echo %GREEN%ALREADY EXISTS%NC%
    call :log "Virtual environment already exists"
    set VENV_STATUS=1
) else (
    echo %YELLOW%CREATING%NC%
    python -m venv "%VENV_DIR%" >> "%LOG_FILE%" 2>&1
    
    if %ERRORLEVEL% == 0 (
        echo %GREEN%OK%NC%
        call :log "Virtual environment created successfully"
        set VENV_STATUS=1
    ) else (
        echo %RED%FAILED%NC%
        echo %RED%Failed to create Python virtual environment.%NC%
        echo %YELLOW%Check that Python 3.9+ is installed.%NC%
        call :log "Failed to create virtual environment"
        set VENV_STATUS=0
    )
)
exit /b %VENV_STATUS%

REM Install MCP SDK
:install_mcp
call :log "Installing MCP SDK"
echo %YELLOW%Installing MCP SDK... %NC%

"%VENV_DIR%\Scripts\pip" install "mcp[cli]" >> "%LOG_FILE%" 2>&1

if %ERRORLEVEL% == 0 (
    echo %GREEN%OK%NC%
    call :log "MCP SDK installed successfully"
    set MCP_STATUS=1
) else (
    echo %RED%FAILED%NC%
    echo %RED%Failed to install MCP SDK.%NC%
    echo %YELLOW%Check the log file for details: %LOG_FILE%%NC%
    call :log "Failed to install MCP SDK"
    set MCP_STATUS=0
)
exit /b %MCP_STATUS%

REM Set environment variables
:setup_env_vars
call :log "Setting up environment variables"
echo %YELLOW%Setting up environment variables... %NC%

REM Generate environment variables file
set "ENV_FILE=%INSTALL_DIR%\.env.bat"
(
    echo @echo off
    echo set "RESOLVE_SCRIPT_API=C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    echo set "RESOLVE_SCRIPT_LIB=C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    echo set "PYTHONPATH=%%PYTHONPATH%%;%%RESOLVE_SCRIPT_API%%\Modules"
) > "%ENV_FILE%"

REM Source the environment variables
call "%ENV_FILE%"

echo %GREEN%OK%NC%
call :log "Environment variables set:"
call :log "RESOLVE_SCRIPT_API=%RESOLVE_SCRIPT_API%"
call :log "RESOLVE_SCRIPT_LIB=%RESOLVE_SCRIPT_LIB%"

REM Suggest adding to system variables
echo %YELLOW%Consider adding these environment variables to your system:%NC%
echo %BLUE%  RESOLVE_SCRIPT_API = C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting%NC%
echo %BLUE%  RESOLVE_SCRIPT_LIB = C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll%NC%
echo %BLUE%  Add to PYTHONPATH: %%RESOLVE_SCRIPT_API%%\Modules%NC%

exit /b 1

REM Setup Cursor MCP configuration
:setup_cursor_config
call :log "Setting up Cursor MCP configuration"
echo %YELLOW%Setting up Cursor MCP configuration... %NC%

REM Create system-level directory if it doesn't exist
if not exist "%CURSOR_CONFIG_DIR%" mkdir "%CURSOR_CONFIG_DIR%"

REM Create system-level config file with the absolute paths
(
    echo {
    echo   "mcpServers": {
    echo     "davinci-resolve": {
    echo       "name": "DaVinci Resolve MCP",
    echo       "command": "%INSTALL_DIR:\=\\%\\venv\\Scripts\\python.exe",
    echo       "args": ["%INSTALL_DIR:\=\\%\\src\__main__.py"]
    echo     }
    echo   }
    echo }
) > "%CURSOR_CONFIG_FILE%"

REM Create project-level directory if it doesn't exist
if not exist "%PROJECT_CURSOR_DIR%" mkdir "%PROJECT_CURSOR_DIR%"

REM Create project-level config with absolute paths (same as system-level config)
(
    echo {
    echo   "mcpServers": {
    echo     "davinci-resolve": {
    echo       "name": "DaVinci Resolve MCP",
    echo       "command": "%INSTALL_DIR:\=\\%\\venv\\Scripts\\python.exe",
    echo       "args": ["%INSTALL_DIR:\=\\%\\src\__main__.py"]
    echo     }
    echo   }
    echo }
) > "%PROJECT_CONFIG_FILE%"

if exist "%CURSOR_CONFIG_FILE%" if exist "%PROJECT_CONFIG_FILE%" (
    echo %GREEN%OK%NC%
    echo %GREEN%Cursor MCP config created at: %CURSOR_CONFIG_FILE%%NC%
    echo %GREEN%Project MCP config created at: %PROJECT_CONFIG_FILE%%NC%
    call :log "Cursor MCP configuration created successfully"
    call :log "System config file: %CURSOR_CONFIG_FILE%"
    call :log "Project config file: %PROJECT_CONFIG_FILE%"
    
    REM Show the paths that were set
    echo %YELLOW%Paths configured:%NC%
    echo %BLUE%  Python: %INSTALL_DIR%\venv\Scripts\python.exe%NC%
    echo %BLUE%  Script: %INSTALL_DIR%\src\__main__.py%NC%
    
    set CONFIG_STATUS=1
) else (
    echo %RED%FAILED%NC%
    echo %RED%Failed to create Cursor MCP configuration.%NC%
    call :log "Failed to create Cursor MCP configuration"
    set CONFIG_STATUS=0
)
exit /b %CONFIG_STATUS%

REM Verify installation
:verify_installation
call :log "Verifying installation"
echo %BLUE%%BOLD%=================================================%NC%
echo %YELLOW%%BOLD%Verifying installation...%NC%

REM Run the verification script
call "%INSTALL_DIR%\scripts\verify-installation.bat"
set VERIFY_RESULT=%ERRORLEVEL%

call :log "Verification completed with result: %VERIFY_RESULT%"

exit /b %VERIFY_RESULT%

REM Run server if verification succeeds
:run_server
call :log "Starting server"
echo %BLUE%%BOLD%=================================================%NC%
echo %GREEN%%BOLD%Starting DaVinci Resolve MCP Server...%NC%
echo.

REM Run the server using the virtual environment
"%VENV_DIR%\Scripts\python.exe" "%INSTALL_DIR%\src\__main__.py"

set SERVER_EXIT=%ERRORLEVEL%
call :log "Server exited with code: %SERVER_EXIT%"

exit /b %SERVER_EXIT%

REM Main installation process
:main
call :log "Starting installation process"

REM Check if DaVinci Resolve is running
call :check_resolve_running
if %RESOLVE_RUNNING% == 0 (
    echo %YELLOW%Waiting 10 seconds for DaVinci Resolve to start...%NC%
    timeout /t 10 /nobreak > nul
    call :check_resolve_running
    if %RESOLVE_RUNNING% == 0 (
        call :log "Installation aborted - DaVinci Resolve not running"
        echo %RED%Installation aborted.%NC%
        exit /b 1
    )
)

REM Create virtual environment
call :create_venv
if %VENV_STATUS% == 0 (
    call :log "Installation aborted - virtual environment setup failed"
    echo %RED%Installation aborted.%NC%
    exit /b 1
)

REM Install MCP SDK
call :install_mcp
if %MCP_STATUS% == 0 (
    call :log "Installation aborted - MCP SDK installation failed"
    echo %RED%Installation aborted.%NC%
    exit /b 1
)

REM Set up environment variables
call :setup_env_vars

REM Set up Cursor configuration
call :setup_cursor_config
if %CONFIG_STATUS% == 0 (
    call :log "Installation aborted - Cursor configuration failed"
    echo %RED%Installation aborted.%NC%
    exit /b 1
)

REM Verify installation
call :verify_installation
set VERIFY_RESULT=%ERRORLEVEL%
if %VERIFY_RESULT% NEQ 0 (
    call :log "Installation completed with verification warnings"
    echo %YELLOW%Installation completed with warnings.%NC%
    echo %YELLOW%Please fix any issues before starting the server.%NC%
    echo %YELLOW%You can run the verification script again:%NC%
    echo %BLUE%  scripts\verify-installation.bat%NC%
    exit /b 1
)

REM Installation successful
call :log "Installation completed successfully"
echo %GREEN%%BOLD%Installation completed successfully!%NC%
echo %YELLOW%You can now start the server with:%NC%
echo %BLUE%  run-now.bat%NC%

REM Ask if the user wants to start the server now
echo.
set /p START_SERVER="Do you want to start the server now? (y/n) "
if /i "%START_SERVER%" == "y" (
    call :run_server
) else (
    call :log "User chose not to start the server"
    echo %YELLOW%You can start the server later with:%NC%
    echo %BLUE%  run-now.bat%NC%
)

exit /b 0

REM Call the main process
call :main 