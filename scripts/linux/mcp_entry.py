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

# Required packages for MCP server
REQUIRED_PACKAGES = ["mcp"]


def check_windows_python_exists() -> tuple[bool, str]:
    """Check if Windows Python is available."""
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-Command", "python --version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "Python not found"
    except Exception as e:
        return False, str(e)


def check_windows_package(python_path: str, package: str) -> bool:
    """Check if a package is installed in Windows Python."""
    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"& '{python_path}' -c \"import {package}\"",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except Exception:
        return False


def check_dependencies(python_path: str) -> tuple[bool, list[str]]:
    """Check if all required packages are installed.

    Returns:
        tuple: (all_ok, list of missing packages)
    """
    missing = []
    for pkg in REQUIRED_PACKAGES:
        if not check_windows_package(python_path, pkg):
            missing.append(pkg)
    return len(missing) == 0, missing


def get_wsl_unc_path() -> str:
    """Get the UNC path to access WSL from Windows."""
    # Get distro name
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.strip().split("=")[1].strip('"')
                    # Capitalize first letter for Windows UNC path
                    distro = distro.capitalize()
                    break
            else:
                distro = "Ubuntu"  # Default
    except Exception:
        distro = "Ubuntu"

    project_root = get_project_root()
    # Convert /home/user/path to \\wsl$\Distro\home\user\path
    win_path = str(project_root).replace("/", "\\")
    return f"\\\\wsl$\\{distro}{win_path}"


def print_dependency_error(python_path: str, missing_packages: list[str]):
    """Print error message for missing dependencies."""
    print("\n[MCP] ERROR: Missing required Python packages on Windows!", file=sys.stderr)
    print(f"[MCP] Python: {python_path}", file=sys.stderr)
    print(f"[MCP] Missing: {', '.join(missing_packages)}", file=sys.stderr)
    print("", file=sys.stderr)
    print("[MCP] To fix, run in PowerShell:", file=sys.stderr)
    print(f"  {python_path} -m pip install {' '.join(missing_packages)}", file=sys.stderr)
    print("", file=sys.stderr)
    print("[MCP] Or install all requirements:", file=sys.stderr)
    win_project = get_wsl_unc_path()
    print(f'  {python_path} -m pip install -r "{win_project}\\requirements.txt"', file=sys.stderr)
    print("", file=sys.stderr)


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


def wsl_to_win_path(wsl_path: str) -> str:
    """Convert WSL path to Windows path. /mnt/c/foo -> C:\\foo"""
    if wsl_path.startswith("/mnt/") and len(wsl_path) > 6:
        drive = wsl_path[5].upper()
        rest = wsl_path[6:].replace("/", "\\")
        return f"{drive}:{rest}"
    return wsl_path


def find_windows_python(project_dir: str, verbose: bool = False) -> tuple[str, str | None]:
    """Find Python executable, checking multiple venv locations.

    Returns:
        tuple: (python_path, venv_name or None if using system Python)
    """
    # Check common venv names in order of preference
    venv_names = [".venv_win", ".venv", "venv", ".env"]

    for venv_name in venv_names:
        python_path = f"{project_dir}\\{venv_name}\\Scripts\\python.exe"
        wsl_check_path = win_to_wsl_path(python_path)
        try:
            if Path(wsl_check_path).exists():
                return python_path, venv_name
        except OSError:
            # WSL may throw errors when checking paths that don't exist
            continue

    # Fallback: system Python on Windows
    return "python", None


def print_venv_setup_instructions(project_dir: str):
    """Print instructions for setting up Windows venv from WSL."""
    print("\n[MCP] No Windows Python venv found.", file=sys.stderr)
    print("[MCP] For best results, create a Windows venv:", file=sys.stderr)
    print("", file=sys.stderr)
    print("  # In PowerShell (as Administrator):", file=sys.stderr)
    print(f'  cd "{project_dir}"', file=sys.stderr)
    print("  python -m venv .venv_win", file=sys.stderr)
    print("  .\\.venv_win\\Scripts\\pip install -r requirements.txt", file=sys.stderr)
    print("", file=sys.stderr)
    print("[MCP] Falling back to system Python...", file=sys.stderr)


def get_windows_paths(config: dict, verbose: bool = False) -> dict:
    """Get Windows paths from config or auto-detect."""
    # Auto-detect project path from this script's location
    project_root = get_project_root()
    win_project = config.get("RESOLVE_MCP_PROJECT") or wsl_to_win_path(str(project_root))

    # Auto-detect Python
    if config.get("RESOLVE_MCP_PYTHON"):
        win_python = config["RESOLVE_MCP_PYTHON"]
        venv_name = "configured"
    else:
        win_python, venv_name = find_windows_python(win_project, verbose)
        if venv_name is None:
            print_venv_setup_instructions(win_project)

    return {
        "project": win_project,
        "python": win_python,
        "venv": venv_name,
        "script": f"{win_project}\\src\\__main__.py",
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

    # Always show status to stderr (doesn't interfere with MCP stdio protocol)
    print("[MCP] Initializing WSL bridge to Windows...", file=sys.stderr)

    # Load config from .env
    config = load_env_config()
    paths = get_windows_paths(config, verbose)

    # Check dependencies before proceeding
    print("[MCP] Checking dependencies...", file=sys.stderr)
    deps_ok, missing = check_dependencies(paths["python"])
    if not deps_ok:
        print_dependency_error(paths["python"], missing)
        return 1
    print("[MCP] Dependencies OK", file=sys.stderr)

    # Check if Resolve is running
    if not check_resolve_running(verbose):
        print("[MCP] Starting DaVinci Resolve...", file=sys.stderr)
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
        for i in range(30):
            time.sleep(2)
            if check_resolve_running(verbose=False):
                print("[MCP] DaVinci Resolve started, waiting for API...", file=sys.stderr)
                time.sleep(10)  # Extra time for API
                break
            if i % 5 == 0:
                print(f"[MCP] Waiting for Resolve... ({i * 2}s)", file=sys.stderr)
        else:
            print("[MCP] ERROR: Timeout waiting for DaVinci Resolve", file=sys.stderr)
            return 1
    else:
        print("[MCP] DaVinci Resolve is running", file=sys.stderr)

    venv_info = f" (from {paths['venv']}/)" if paths["venv"] else " (system)"
    print(f"[MCP] Using Python{venv_info}: {paths['python']}", file=sys.stderr)
    print("[MCP] Starting server (stdio mode)...", file=sys.stderr)

    if verbose:
        print(f"[MCP] Project: {paths['project']}", file=sys.stderr)
        print(f"[MCP] Script: {paths['script']}", file=sys.stderr)

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
