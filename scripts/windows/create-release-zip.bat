@echo off
REM create-release-zip.bat
REM Script to create a versioned zip file for distribution on Windows

setlocal EnableDelayedExpansion

REM Colors for terminal output
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set RED=[91m
set NC=[0m

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Get version from VERSION.md
for /f "tokens=3" %%i in ('findstr /B /C:"Current Version:" "%PROJECT_ROOT%\docs\VERSION.md"') do (
    set "VERSION=%%i"
    goto :version_found
)
:version_found

if "%VERSION%"=="" (
    echo %RED%Error: Could not determine version from VERSION.md%NC%
    exit /b 1
)

REM Create filename with version
set "ZIP_FILE=davinci-resolve-mcp-v%VERSION%.zip"
set "DIST_DIR=%PROJECT_ROOT%\dist"
set "ZIP_PATH=%DIST_DIR%\%ZIP_FILE%"

REM Ensure dist directory exists
if not exist "%DIST_DIR%" mkdir "%DIST_DIR%"

echo %BLUE%=================================================%NC%
echo %BLUE%  Creating Release Zip for DaVinci Resolve MCP   %NC%
echo %BLUE%=================================================%NC%
echo %YELLOW%Version: %VERSION%%NC%
echo %YELLOW%Output file: %ZIP_FILE%%NC%
echo %YELLOW%Output directory: %DIST_DIR%%NC%
echo.

REM Change to project root directory
cd /d "%PROJECT_ROOT%" || exit /b 1

REM Check if 7-Zip is installed
where 7z >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %YELLOW%7-Zip not found, using PowerShell to create zip file%NC%
    
    REM Create temporary file list
    git ls-files > filelist.txt
    git ls-files --others --exclude-standard >> filelist.txt
    
    REM Use PowerShell to create the zip file
    powershell -Command "Add-Type -Assembly System.IO.Compression.FileSystem; $zipFile = [System.IO.Compression.ZipFile]::Open('%ZIP_PATH%', [System.IO.Compression.ZipArchiveMode]::Create); Get-Content filelist.txt | ForEach-Object { if (Test-Path -Path $_ -PathType Leaf) { $file = $_; $entry = $zipFile.CreateEntry($file); $stream = $entry.Open(); $bytes = [System.IO.File]::ReadAllBytes($file); $stream.Write($bytes, 0, $bytes.Length); $stream.Close() } }; $zipFile.Dispose()"
    
    REM Remove temporary file list
    del filelist.txt
) else (
    echo %YELLOW%Using 7-Zip to create zip file...%NC%
    
    REM Create temporary file list
    git ls-files > filelist.txt
    git ls-files --others --exclude-standard >> filelist.txt
    
    REM Use 7-Zip to create the zip file
    7z a -tzip "%ZIP_PATH%" @filelist.txt
    
    REM Remove temporary file list
    del filelist.txt
)

REM Check if the zip file was created successfully
if exist "%ZIP_PATH%" (
    echo %GREEN%Successfully created release zip: %ZIP_PATH%%NC%
) else (
    echo %RED%Failed to create release zip%NC%
    exit /b 1
)

echo %GREEN%Release zip created successfully!%NC%

exit /b 0 