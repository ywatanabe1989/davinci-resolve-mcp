# DaVinci Resolve MCP - Windows Automated Setup
# Run as Administrator in PowerShell

param(
    [string]$WslDistro = "Ubuntu",
    [string]$WslProjectPath = "/home/ywatanabe/proj/davinci-resolve-mcp",
    [string]$WindowsInstallPath = "C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp"
)

$ErrorActionPreference = "Stop"

Write-Host "=== DaVinci Resolve MCP Windows Setup ===" -ForegroundColor Cyan

# Check admin privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: Run as Administrator" -ForegroundColor Red
    exit 1
}

# Check if DaVinci Resolve is installed
$ResolvePath = "C:\Program Files\Blackmagic Design\DaVinci Resolve"
if (-NOT (Test-Path $ResolvePath)) {
    Write-Host "ERROR: DaVinci Resolve not found at $ResolvePath" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] DaVinci Resolve found" -ForegroundColor Green

# Check Python
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-NOT $PythonPath) {
    Write-Host "ERROR: Python not found. Install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}
$PythonVersion = python --version
Write-Host "[OK] $PythonVersion found at $PythonPath" -ForegroundColor Green

# WSL source path
$WslPath = "\\wsl$\$WslDistro$WslProjectPath"
if (-NOT (Test-Path $WslPath)) {
    Write-Host "ERROR: WSL path not found: $WslPath" -ForegroundColor Red
    Write-Host "  Ensure WSL is running and project exists at $WslProjectPath" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] WSL project found at $WslPath" -ForegroundColor Green

# Create parent directory if needed
$ParentDir = Split-Path $WindowsInstallPath -Parent
if (-NOT (Test-Path $ParentDir)) {
    New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
    Write-Host "[OK] Created $ParentDir" -ForegroundColor Green
}

# Remove existing installation (backup first)
if (Test-Path $WindowsInstallPath) {
    $BackupPath = "${WindowsInstallPath}_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Move-Item $WindowsInstallPath $BackupPath -Force
    Write-Host "[OK] Backed up existing installation to $BackupPath" -ForegroundColor Yellow
}

# Create symlink to WSL
cmd /c mklink /D "$WindowsInstallPath" "$WslPath"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create symlink" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Symlink created: $WindowsInstallPath -> $WslPath" -ForegroundColor Green

# Create Windows venv
$VenvPath = "$WindowsInstallPath\venv"
Write-Host "Creating Windows virtual environment..." -ForegroundColor Cyan
python -m venv $VenvPath
if (-NOT (Test-Path "$VenvPath\Scripts\python.exe")) {
    Write-Host "ERROR: Failed to create venv" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Virtual environment created" -ForegroundColor Green

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Cyan
& "$VenvPath\Scripts\pip" install --quiet --upgrade pip
& "$VenvPath\Scripts\pip" install --quiet mcp httpx

# Verify installation
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
& "$VenvPath\Scripts\python" -c "import mcp; print('[OK] MCP module available')"

Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "Next: Restart Claude Code and reconnect MCP server" -ForegroundColor Yellow
Write-Host "  /mcp reconnect davinci-resolve" -ForegroundColor White
