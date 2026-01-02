# Pre-launch Check Script for DaVinci Resolve MCP (Windows Version)
# This script verifies that DaVinci Resolve is running and all required components are installed
# before launching Cursor or Claude Desktop

# Functions for colored output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Red($message) { Write-ColorOutput "Red" $message }
function Write-Green($message) { Write-ColorOutput "Green" $message }
function Write-Yellow($message) { Write-ColorOutput "Yellow" $message }
function Write-Blue($message) { Write-ColorOutput "Blue" $message }

# Path configurations
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RootDir = Split-Path -Parent $ScriptDir
$VenvDir = Join-Path -Path $RootDir -ChildPath "venv"
$CursorConfigFile = Join-Path -Path $env:APPDATA -ChildPath "Cursor\mcp.json"
$ResolveMcpServer = Join-Path -Path $RootDir -ChildPath "src\__main__.py"

# Default paths for DaVinci Resolve on Windows
$DefaultResolveApiPath = Join-Path -Path $env:PROGRAMDATA -ChildPath "Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$DefaultResolveLibPath = Join-Path -Path ${env:PROGRAMFILES} -ChildPath "Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$DefaultResolveModulesPath = Join-Path -Path $DefaultResolveApiPath -ChildPath "Modules"

# List of required files with permissions
$RequiredFiles = @(
    @{Path = (Join-Path -Path $RootDir -ChildPath "src\__main__.py"); RequiredExists = $true},
    @{Path = (Join-Path -Path $RootDir -ChildPath "scripts\run-now.sh"); RequiredExists = $false}  # Optional file for Windows
)

# Function to check if DaVinci Resolve is running
function Test-ResolveRunning {
    $resolveProcess = Get-Process -Name "Resolve" -ErrorAction SilentlyContinue
    if ($resolveProcess) {
        Write-Green "✓ DaVinci Resolve is running"
        return $true
    }
    
    $davinciProcess = Get-Process -Name "DaVinci Resolve" -ErrorAction SilentlyContinue
    if ($davinciProcess) {
        Write-Green "✓ DaVinci Resolve is running"
        return $true
    }
    
    Write-Red "✗ DaVinci Resolve is NOT running"
    Write-Yellow "Please start DaVinci Resolve before launching Cursor or Claude Desktop"
    return $false
}

# Function to check environment variables
function Test-ResolveEnv {
    $resolveScriptApi = $env:RESOLVE_SCRIPT_API
    $resolveScriptLib = $env:RESOLVE_SCRIPT_LIB
    
    if (-not $resolveScriptApi -or -not $resolveScriptLib) {
        return $false
    }
    
    return $true
}

# Function to set environment variables
function Set-ResolveEnvironment {
    $env:RESOLVE_SCRIPT_API = $DefaultResolveApiPath
    $env:RESOLVE_SCRIPT_LIB = $DefaultResolveLibPath
    
    # Update PYTHONPATH
    if ($env:PYTHONPATH) {
        if (-not $env:PYTHONPATH.Contains($DefaultResolveModulesPath)) {
            $env:PYTHONPATH += ";$DefaultResolveModulesPath"
        }
    }
    else {
        $env:PYTHONPATH = $DefaultResolveModulesPath
    }
    
    # Store variables for system
    [System.Environment]::SetEnvironmentVariable("RESOLVE_SCRIPT_API", $DefaultResolveApiPath, "User")
    [System.Environment]::SetEnvironmentVariable("RESOLVE_SCRIPT_LIB", $DefaultResolveLibPath, "User")
    
    # Get current PYTHONPATH from system
    $currentPythonPath = [System.Environment]::GetEnvironmentVariable("PYTHONPATH", "User")
    if ($currentPythonPath) {
        if (-not $currentPythonPath.Contains($DefaultResolveModulesPath)) {
            $updatedPythonPath = "$currentPythonPath;$DefaultResolveModulesPath"
            [System.Environment]::SetEnvironmentVariable("PYTHONPATH", $updatedPythonPath, "User")
        }
    }
    else {
        [System.Environment]::SetEnvironmentVariable("PYTHONPATH", $DefaultResolveModulesPath, "User")
    }
}

# Function to check if virtual environment exists and has MCP installed
function Test-VirtualEnv {
    if (-not (Test-Path -Path $VenvDir)) {
        return 1  # Missing venv
    }
    
    $pythonPath = Join-Path -Path $VenvDir -ChildPath "Scripts\python.exe"
    if (-not (Test-Path -Path $pythonPath)) {
        return 1  # Missing Python
    }
    
    $pipPath = Join-Path -Path $VenvDir -ChildPath "Scripts\pip.exe"
    $mcpInstalled = & $pipPath list | Select-String -Pattern "mcp"
    
    if (-not $mcpInstalled) {
        return 2  # Missing MCP
    }
    
    return 0  # All good
}

# Function to check required files
function Test-RequiredFiles {
    $missingFiles = @()
    
    foreach ($file in $RequiredFiles) {
        if ($file.RequiredExists -eq $true -and -not (Test-Path -Path $file.Path)) {
            $missingFiles += $file.Path
        }
    }
    
    return $missingFiles
}

# Function to check Cursor config
function Test-CursorConfig {
    if (-not (Test-Path -Path $CursorConfigFile)) {
        return 1  # Missing config file
    }
    
    $configContent = Get-Content -Path $CursorConfigFile -Raw -ErrorAction SilentlyContinue
    if (-not $configContent -or (-not $configContent.Contains("davinci-resolve"))) {
        return 2  # Missing DaVinci Resolve config
    }
    
    return 0  # All good
}

# Function to create Cursor config
function Set-CursorConfig {
    # Create directory if it doesn't exist
    $configDir = Split-Path -Parent $CursorConfigFile
    if (-not (Test-Path -Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    
    # Python path in virtual environment for Windows
    $pythonPath = Join-Path -Path $VenvDir -ChildPath "Scripts\python.exe"
    $pythonPath = $pythonPath.Replace("\", "\\")
    $serverPath = (Join-Path -Path $RootDir -ChildPath "src\__main__.py").Replace("\", "\\")
    
    # Create config file
    $configContent = @"
{
  "mcpServers": {
    "davinci-resolve": {
      "name": "DaVinci Resolve MCP",
      "command": "$pythonPath",
      "args": ["$serverPath"]
    }
  }
}
"@
    
    $configContent | Out-File -FilePath $CursorConfigFile -Encoding utf8 -Force
    Write-Green "✓ Cursor configuration created"
}

# Function to update Cursor config
function Update-CursorConfig {
    # Backup existing config
    Copy-Item -Path $CursorConfigFile -Destination "$CursorConfigFile.bak" -Force
    
    # Python path in virtual environment for Windows
    $pythonPath = Join-Path -Path $VenvDir -ChildPath "Scripts\python.exe"
    $pythonPath = $pythonPath.Replace("\", "\\")
    $serverPath = (Join-Path -Path $RootDir -ChildPath "src\__main__.py").Replace("\", "\\")
    
    try {
        # Read existing config
        $configJson = Get-Content -Path $CursorConfigFile | ConvertFrom-Json
        
        # Check if mcpServers exists
        if (-not $configJson.mcpServers) {
            $configJson | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
        }
        
        # Add or update davinci-resolve server
        $configJson.mcpServers | Add-Member -MemberType NoteProperty -Name "davinci-resolve" -Value @{
            "name" = "DaVinci Resolve MCP"
            "command" = $pythonPath
            "args" = @($serverPath)
        } -Force
        
        # Save config
        $configJson | ConvertTo-Json -Depth 4 | Out-File -FilePath $CursorConfigFile -Encoding utf8 -Force
        Write-Green "✓ Cursor configuration updated"
    }
    catch {
        # If error occurs, create a new config file
        Write-Yellow "Error updating Cursor config. Creating a new config file..."
        Set-CursorConfig
    }
}

# Main section starts here
Write-Host ""
Write-Blue "================================================="
Write-Blue "  DaVinci Resolve MCP Pre-Launch Check (Windows Version)     "
Write-Blue "================================================="
Write-Host ""

# Check if the script is running as admin
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Yellow "Note: This script is not running as administrator. Some operations may be limited."
    Write-Host ""
}

Write-Yellow "Performing pre-launch checks for DaVinci Resolve MCP..."
Write-Host "Version: 1.3.8 - Windows Support"
Write-Host ""

# Check 1: Required files
Write-Yellow "Checking required files..."
$missingFiles = Test-RequiredFiles
if ($missingFiles.Count -eq 0) {
    Write-Green "✓ All required files are present"
}
else {
    Write-Red "✗ Some required files are missing:"
    foreach ($file in $missingFiles) {
        Write-Output "  - $file"
    }
    
    Write-Yellow "Creating server file if missing..."
    # Create src\__main__.py if it's missing
    if (-not (Test-Path -Path $ResolveMcpServer)) {
        Write-Yellow "Creating basic src\__main__.py..."
        $serverContent = @'
#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server
A server that connects to DaVinci Resolve via the Model Context Protocol (MCP)

Version: 1.3.8 - Windows Support
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import platform utilities
from src.utils.platform import setup_environment, get_platform, get_resolve_paths

# Setup platform-specific paths and environment variables
paths = get_resolve_paths()
RESOLVE_API_PATH = paths["api_path"]
RESOLVE_LIB_PATH = paths["lib_path"]
RESOLVE_MODULES_PATH = paths["modules_path"]

os.environ["RESOLVE_SCRIPT_API"] = RESOLVE_API_PATH
os.environ["RESOLVE_SCRIPT_LIB"] = RESOLVE_LIB_PATH

# Add the module path to Python's path if it's not already there
if RESOLVE_MODULES_PATH not in sys.path:
    sys.path.append(RESOLVE_MODULES_PATH)

# Import MCP
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("davinci-resolve-mcp")

# Log server version and platform
VERSION = "1.3.8"
logger.info(f"Starting DaVinci Resolve MCP Server v{VERSION}")
logger.info(f"Detected platform: {get_platform()}")
logger.info(f"Using Resolve API path: {RESOLVE_API_PATH}")
logger.info(f"Using Resolve library path: {RESOLVE_LIB_PATH}")

# Create MCP server instance
mcp = FastMCP("DaVinciResolveMCP")

# Start the server
if __name__ == "__main__":
    logger.info("Starting DaVinci Resolve MCP Server")
    mcp.run()
'@
        $serverContent | Out-File -FilePath $ResolveMcpServer -Encoding utf8 -Force
        Write-Green "✓ Created src\__main__.py"
    }
}

# Check 2: DaVinci Resolve is running
Write-Yellow "Checking if DaVinci Resolve is running..."
$resolveRunning = Test-ResolveRunning
if (-not $resolveRunning) {
    $startResolve = Read-Host "Would you like to start DaVinci Resolve now? (y/n)"
    if ($startResolve -eq "y" -or $startResolve -eq "Y") {
        Write-Yellow "Starting DaVinci Resolve..."
        
        # Try to locate DaVinci Resolve executable
        $resolveExe = Join-Path -Path ${env:PROGRAMFILES} -ChildPath "Blackmagic Design\DaVinci Resolve\Resolve.exe"
        if (-not (Test-Path -Path $resolveExe)) {
            $resolveExe = "C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
        }
        
        if (Test-Path -Path $resolveExe) {
            Start-Process -FilePath $resolveExe
            Write-Yellow "Waiting for DaVinci Resolve to start..."
            Start-Sleep -Seconds 5
            
            # Check again
            if (Test-ResolveRunning) {
                Write-Green "✓ DaVinci Resolve started successfully"
            }
            else {
                Write-Yellow "DaVinci Resolve is starting. Please wait until it's fully loaded before proceeding."
            }
        }
        else {
            Write-Red "Could not find DaVinci Resolve executable. Please start it manually."
            Write-Yellow "Search paths tried:"
            Write-Yellow "  - $resolveExe"
        }
    }
    else {
        Write-Red "DaVinci Resolve must be running for the MCP server to function properly."
    }
}

# Check 3: Environment variables
Write-Yellow "Checking Resolve environment variables..."
if (Test-ResolveEnv) {
    Write-Green "✓ Resolve environment variables are set"
    Write-Output "  RESOLVE_SCRIPT_API = $env:RESOLVE_SCRIPT_API"
    Write-Output "  RESOLVE_SCRIPT_LIB = $env:RESOLVE_SCRIPT_LIB"
}
else {
    Write-Red "✗ Resolve environment variables are NOT set"
    Write-Yellow "Setting default environment variables..."
    
    Set-ResolveEnvironment
    
    Write-Green "✓ Environment variables set for this session and permanently:"
    Write-Output "  RESOLVE_SCRIPT_API = $env:RESOLVE_SCRIPT_API"
    Write-Output "  RESOLVE_SCRIPT_LIB = $env:RESOLVE_SCRIPT_LIB"
    Write-Output "  PYTHONPATH includes = $DefaultResolveModulesPath"
}

# Check 4: Python and Virtual environment
Write-Yellow "Checking Python and virtual environment..."
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Red "✗ Python is not installed or not in your PATH"
    Write-Yellow "Please install Python 3.6+ and make sure it's in your PATH"
    Write-Output "Download from: https://www.python.org/downloads/"
}
else {
    $pythonVersion = & python --version
    Write-Green "✓ Python installed: $pythonVersion"
    
    # Check virtual environment
    $venvStatus = Test-VirtualEnv
    if ($venvStatus -eq 0) {
        Write-Green "✓ Virtual environment is set up correctly with MCP installed"
    }
    elseif ($venvStatus -eq 2) {
        Write-Red "✗ MCP is not installed in the virtual environment"
        Write-Yellow "Installing MCP..."
        
        $pipPath = Join-Path -Path $VenvDir -ChildPath "Scripts\pip.exe"
        & $pipPath install "mcp[cli]"
        
        Write-Green "✓ MCP installed"
    }
    else {
        Write-Red "✗ Virtual environment is missing or incomplete"
        Write-Yellow "Setting up virtual environment..."
        
        # Create virtual environment directory if it doesn't exist
        if (-not (Test-Path -Path $VenvDir)) {
            New-Item -ItemType Directory -Path $VenvDir -Force | Out-Null
        }
        
        # Create virtual environment
        python -m venv $VenvDir
        
        # Install MCP
        $pipPath = Join-Path -Path $VenvDir -ChildPath "Scripts\pip.exe"
        & $pipPath install "mcp[cli]"
        
        Write-Green "✓ Virtual environment created and MCP installed"
    }
}

# Check 5: Cursor configuration
Write-Yellow "Checking Cursor configuration..."
$cursorStatus = Test-CursorConfig
if ($cursorStatus -eq 0) {
    Write-Green "✓ Cursor is configured to use the DaVinci Resolve MCP server"
}
elseif ($cursorStatus -eq 1) {
    Write-Red "✗ Cursor configuration file is missing"
    Write-Yellow "Creating Cursor configuration..."
    Set-CursorConfig
}
else {
    Write-Red "✗ Cursor configuration is missing DaVinci Resolve MCP settings"
    Write-Yellow "Updating Cursor configuration..."
    Update-CursorConfig
}

# Final message
Write-Output ""
Write-Green "All checks complete!"
Write-Green "Your system is ready to use DaVinci Resolve with Cursor or Claude Desktop."
Write-Output ""

# Ask if user wants to launch Cursor
$launchCursor = Read-Host "Would you like to launch Cursor now? (y/n)"
if ($launchCursor -eq "y" -or $launchCursor -eq "Y") {
    Write-Yellow "Launching Cursor..."
    
    # Try to launch Cursor
    $cursorPath = Join-Path -Path ${env:LOCALAPPDATA} -ChildPath "Programs\Cursor\Cursor.exe"
    if (Test-Path -Path $cursorPath) {
        Start-Process -FilePath $cursorPath
        Write-Green "Cursor launched. Enjoy using DaVinci Resolve with AI assistance!"
    }
    else {
        Write-Yellow "Could not find Cursor executable at: $cursorPath"
        Write-Yellow "Please launch Cursor manually."
    }
} 