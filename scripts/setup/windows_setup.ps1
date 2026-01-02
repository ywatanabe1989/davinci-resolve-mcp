# DaVinci Resolve MCP - Windows Setup Script
# Run from Admin PowerShell: .\scripts\setup\windows_setup.ps1

$ErrorActionPreference = "Stop"

$ProjectPath = "C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp"
$VenvPath = "$ProjectPath\.venv_win"

Write-Host "=== DaVinci Resolve MCP Windows Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some operations may fail." -ForegroundColor Yellow
}

# Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Check project path
Write-Host "[2/4] Checking project path..." -ForegroundColor Yellow
if (Test-Path $ProjectPath) {
    Write-Host "  Found: $ProjectPath" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Project not found at $ProjectPath" -ForegroundColor Red
    exit 1
}

# Create/recreate venv
Write-Host "[3/4] Creating virtual environment (.venv_win)..." -ForegroundColor Yellow
Set-Location $ProjectPath

# Remove existing .venv_win if it exists
if (Test-Path $VenvPath) {
    Write-Host "  Removing existing .venv_win..." -ForegroundColor Gray
    # Force remove all contents first
    Get-ChildItem $VenvPath -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    # Then remove the directory itself
    Remove-Item -Recurse -Force $VenvPath -ErrorAction SilentlyContinue
    # Handle symlinks/junctions as fallback
    if (Test-Path $VenvPath) {
        cmd /c "rmdir /s /q `"$VenvPath`"" 2>$null
    }
}

# Create fresh venv
python -m venv $VenvPath
if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
    Write-Host "  ERROR: Failed to create venv" -ForegroundColor Red
    exit 1
}
Write-Host "  Created: $VenvPath" -ForegroundColor Green

# Install dependencies
Write-Host "[4/4] Installing dependencies..." -ForegroundColor Yellow
& "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip --quiet
& "$VenvPath\Scripts\pip.exe" install "mcp[cli]" requests psutil jsonrpcserver --quiet

# Verify installation
$mcpInstalled = & "$VenvPath\Scripts\python.exe" -c "import mcp; print('OK')" 2>&1
if ($mcpInstalled -eq "OK") {
    Write-Host "  Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host "  $mcpInstalled" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Start DaVinci Resolve"
Write-Host "  2. From WSL, run: python3 mcp-entry --verbose"
Write-Host "  3. Or reconnect the MCP server in Claude Code"
Write-Host ""
