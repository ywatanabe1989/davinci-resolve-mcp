#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server - WSL Entry Point

Automatically detects environment (WSL vs Windows) and launches appropriately.
For MCP stdio communication, all status output goes to stderr only when verbose.

Usage:
    python scripts/linux/mcp_entry.py           # MCP mode (quiet)
    python scripts/linux/mcp_entry.py --verbose # With status output
"""

import sys
import subprocess
import platform
from pathlib import Path


def is_wsl() -> bool:
    """Detect if running in WSL."""
    if platform.system() != "Linux":
        return False
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False


def get_project_root() -> Path:
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


def load_env_config() -> dict:
    """Load configuration from .env file."""
    config = {}
    env_file = get_project_root() / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    # Remove quotes
                    value = value.strip().strip("'\"")
                    config[key] = value
    return config


def win_to_wsl_path(win_path: str) -> str:
    """Convert Windows path to WSL /mnt/c/ path."""
    # C:\foo\bar -> /mnt/c/foo/bar
    if len(win_path) >= 2 and win_path[1] == ":":
        drive = win_path[0].lower()
        rest = win_path[2:].replace("\\", "/")
        return f"/mnt/{drive}{rest}"
    return win_path


def get_windows_paths(config: dict) -> dict:
    """Get Windows paths from config or defaults."""
    win_project = config.get("RESOLVE_MCP_PROJECT", r"C:\Program Files (x86)\ywatanabe\davinci-resolve-mcp")
    return {
        "project": win_project,
        "python": f"{win_project}\\.venv_win\\Scripts\\python.exe",
        "script": f"{win_project}\\src\\__main__.py",  # Entry point for full tool registration
        "resolve_exe": config.get(
            "RESOLVE_EXE",
            r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe",
        ),
        "api": config.get(
            "RESOLVE_SCRIPT_API",
            r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting",
        ),
        "lib": config.get(
            "RESOLVE_SCRIPT_LIB",
            r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll",
        ),
    }


def check_resolve_running(verbose: bool = False) -> bool:
    """Check if DaVinci Resolve is running on Windows."""
    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "Get-Process -Name 'Resolve' -ErrorAction SilentlyContinue",
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        running = bool(result.stdout.strip())
        if verbose:
            status = "running" if running else "not running"
            print(f"DaVinci Resolve: {status}", file=sys.stderr)
        return running
    except Exception:
        return False


def run_via_wsl(verbose: bool = False) -> int:
    """Run MCP server on Windows from WSL.

    Uses inline PowerShell with ProcessStartInfo for proper stdio handling.
    Direct piping doesn't work across WSL boundary, so we use .NET Process API.
    """
    import time

    # Load config from .env
    config = load_env_config()
    paths = get_windows_paths(config)

    # Check if Resolve is running
    if not check_resolve_running(verbose):
        if verbose:
            print("Starting DaVinci Resolve...", file=sys.stderr)
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"Start-Process '{paths['resolve_exe']}'",
            ],
            capture_output=True,
        )
        # Wait for Resolve to start
        for _ in range(30):
            time.sleep(2)
            if check_resolve_running(verbose=False):
                if verbose:
                    print("DaVinci Resolve started, waiting for API...", file=sys.stderr)
                time.sleep(10)  # Extra time for API
                break
        else:
            print("ERROR: Timeout waiting for DaVinci Resolve", file=sys.stderr)
            return 1

    if verbose:
        print(f"Project: {paths['project']}", file=sys.stderr)
        print(f"Script: {paths['script']}", file=sys.stderr)

    # Build inline PowerShell script for proper stdio handling
    # Uses synchronous reads with threading for continuous bidirectional IO
    ps_script = f"""
$env:PYTHONPATH = '{paths["project"]}'
$env:RESOLVE_SCRIPT_API = '{paths["api"]}'
$env:RESOLVE_SCRIPT_LIB = '{paths["lib"]}'

$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = '{paths["python"]}'
$pinfo.Arguments = '"{paths["script"]}"'
$pinfo.RedirectStandardInput = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $true

$p = New-Object System.Diagnostics.Process
$p.StartInfo = $pinfo
$p.Start() | Out-Null

# Background runspace to read stdout and print it
$stdoutRunspace = [runspacefactory]::CreateRunspace()
$stdoutRunspace.Open()
$stdoutPS = [powershell]::Create()
$stdoutPS.Runspace = $stdoutRunspace
$stdoutPS.AddScript({{
    param($reader)
    while ($true) {{
        $line = $reader.ReadLine()
        if ($null -eq $line) {{ break }}
        [Console]::Out.WriteLine($line)
        [Console]::Out.Flush()
    }}
}}).AddArgument($p.StandardOutput) | Out-Null
$stdoutHandle = $stdoutPS.BeginInvoke()

# Background runspace for stderr
$stderrRunspace = [runspacefactory]::CreateRunspace()
$stderrRunspace.Open()
$stderrPS = [powershell]::Create()
$stderrPS.Runspace = $stderrRunspace
$stderrPS.AddScript({{
    param($reader)
    while ($true) {{
        $line = $reader.ReadLine()
        if ($null -eq $line) {{ break }}
        [Console]::Error.WriteLine($line)
    }}
}}).AddArgument($p.StandardError) | Out-Null
$stderrHandle = $stderrPS.BeginInvoke()

# Main thread: forward stdin
while (-not $p.HasExited) {{
    $line = [Console]::In.ReadLine()
    if ($null -eq $line) {{ break }}
    try {{
        $p.StandardInput.WriteLine($line)
        $p.StandardInput.Flush()
    }} catch {{ break }}
}}

try {{ $p.StandardInput.Close() }} catch {{}}
$p.WaitForExit(30000)

# Cleanup
try {{
    $stdoutPS.Stop()
    $stderrPS.Stop()
    $stdoutRunspace.Close()
    $stderrRunspace.Close()
}} catch {{}}

exit $p.ExitCode
"""

    if verbose:
        print("Using inline PowerShell with ProcessStartInfo", file=sys.stderr)

    # Run PowerShell with the inline script
    process = subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-Command", ps_script],
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr if verbose else subprocess.DEVNULL,
    )

    return process.wait()


def run_native(verbose: bool = False) -> int:
    """Run MCP server natively on Windows."""
    # Add project to path
    project_root = get_project_root()
    sys.path.insert(0, str(project_root))

    # Suppress logging if not verbose
    if not verbose:
        import logging

        logging.disable(logging.CRITICAL)

    # Import and run
    from src.__main__ import main

    return main()


def main():
    """Smart entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    if is_wsl():
        sys.exit(run_via_wsl(verbose))
    else:
        sys.exit(run_native(verbose))


if __name__ == "__main__":
    main()
