#!/usr/bin/env python3
"""
Core keyboard control functions for DaVinci Resolve MCP Server.

Provides the base functionality for sending keyboard input to DaVinci Resolve
via PowerShell on Windows/WSL.

Based on best practices from "Controlling DaVinci Resolve from WSL2" documentation:
- 200ms minimum delay after focusing window
- Focus verification before sending keys
- Retry logic for focus acquisition
- Window title verification to prevent sending keys to wrong window
"""

import subprocess
import platform
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("davinci-resolve-mcp.keyboard_control")

# Configuration constants
FOCUS_DELAY_MS = 200  # Minimum delay after focusing window
FOCUS_RETRY_COUNT = 3  # Number of retries for focus acquisition
FOCUS_RETRY_DELAY_MS = 100  # Delay between focus retries

# Global state for user context preservation
_saved_user_state: Optional[Dict[str, Any]] = None


def is_wsl() -> bool:
    """Check if running in Windows Subsystem for Linux."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except:
        return False


def get_platform_type() -> str:
    """Get the platform type for keyboard control."""
    if platform.system() == "Windows":
        return "windows"
    elif is_wsl():
        return "wsl"
    elif platform.system() == "Darwin":
        return "macos"
    elif platform.system() == "Linux":
        return "linux"
    return "unknown"


def send_key_to_resolve(
    key: str,
    description: str = "",
    focus_delay_ms: int = FOCUS_DELAY_MS,
    retry_count: int = FOCUS_RETRY_COUNT,
    verify_focus: bool = True,
) -> Dict[str, Any]:
    """
    Send a keyboard key to DaVinci Resolve with focus verification.

    Args:
        key: The key to send in SendKeys format (e.g., ' ' for space, '{LEFT}' for left arrow)
        description: Optional description of the action
        focus_delay_ms: Milliseconds to wait after focusing window (default: 200ms)
        retry_count: Number of retries for focus acquisition (default: 3)
        verify_focus: Whether to verify focus before sending keys (default: True)

    Returns:
        Dict with success status and message
    """
    platform_type = get_platform_type()

    if platform_type not in ["windows", "wsl"]:
        return {
            "success": False,
            "error": f"Keyboard control not supported on {platform_type}. Only Windows/WSL supported.",
        }

    # PowerShell script with focus verification and retry logic
    ps_script = f"""
$resolve = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*DaVinci Resolve*' -or $_.ProcessName -eq 'Resolve' }} | Select-Object -First 1
if ($resolve) {{
    Add-Type @'
    using System;
    using System.Runtime.InteropServices;
    public class Win32 {{
        [DllImport("user32.dll")]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")]
        public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    }}
'@

    $targetHandle = $resolve.MainWindowHandle
    $focusAcquired = $false
    $retryCount = {retry_count}
    $focusDelayMs = {focus_delay_ms}
    $retryDelayMs = {FOCUS_RETRY_DELAY_MS}

    # Retry loop for focus acquisition
    for ($i = 0; $i -lt $retryCount; $i++) {{
        [Win32]::SetForegroundWindow($targetHandle) | Out-Null
        Start-Sleep -Milliseconds $focusDelayMs

        # Verify focus if enabled
        if ({str(verify_focus).lower()}) {{
            $currentForeground = [Win32]::GetForegroundWindow()
            $windowTitle = New-Object System.Text.StringBuilder 256
            [Win32]::GetWindowText($currentForeground, $windowTitle, 256) | Out-Null
            $title = $windowTitle.ToString()

            if ($title -like '*DaVinci Resolve*') {{
                $focusAcquired = $true
                break
            }} else {{
                Write-Output "RETRY: Focus on '$title', expected DaVinci Resolve (attempt $($i + 1)/$retryCount)"
                Start-Sleep -Milliseconds $retryDelayMs
            }}
        }} else {{
            $focusAcquired = $true
            break
        }}
    }}

    if (-not $focusAcquired) {{
        Write-Output 'ERROR: Failed to acquire focus on DaVinci Resolve after retries'
        exit
    }}

    # Final focus verification before sending key
    if ({str(verify_focus).lower()}) {{
        $currentForeground = [Win32]::GetForegroundWindow()
        $windowTitle = New-Object System.Text.StringBuilder 256
        [Win32]::GetWindowText($currentForeground, $windowTitle, 256) | Out-Null
        $title = $windowTitle.ToString()

        if ($title -notlike '*DaVinci Resolve*') {{
            Write-Output "ERROR: Focus stolen! Active window is '$title', not DaVinci Resolve. Aborting to prevent sending keys to wrong window."
            exit
        }}
    }}

    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait('{key}')
    Write-Output 'SUCCESS: Sent key to Resolve (focus verified)'
}} else {{
    Write-Output 'ERROR: DaVinci Resolve window not found'
}}
"""

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=15,  # Increased timeout for retries
        )

        output = result.stdout.strip()
        if "SUCCESS" in output:
            action_desc = description if description else f"key '{key}'"
            logger.info(f"Sent {action_desc} to Resolve")
            return {"success": True, "message": f"Successfully sent {action_desc}"}
        elif "RETRY" in output:
            # Log retry attempts for debugging
            for line in output.split("\n"):
                if "RETRY" in line:
                    logger.warning(line)
            if "SUCCESS" in output:
                action_desc = description if description else f"key '{key}'"
                logger.info(f"Sent {action_desc} to Resolve after retries")
                return {
                    "success": True,
                    "message": f"Successfully sent {action_desc} (after retries)",
                }
            else:
                logger.error(f"Failed to send key after retries: {output}")
                return {"success": False, "error": output}
        else:
            logger.error(f"Failed to send key: {output}")
            return {"success": False, "error": output}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout waiting for PowerShell"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def is_resolve_focused() -> Dict[str, Any]:
    """
    Check if DaVinci Resolve is currently the focused window.

    This is useful to avoid stealing focus from the user's current work.

    Returns:
        Dict with 'focused' boolean and current window title
    """
    platform_type = get_platform_type()

    if platform_type not in ["windows", "wsl"]:
        return {"focused": False, "error": f"Not supported on {platform_type}"}

    ps_script = """
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Win32Check {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
}
'@

$foreground = [Win32Check]::GetForegroundWindow()
$windowTitle = New-Object System.Text.StringBuilder 256
[Win32Check]::GetWindowText($foreground, $windowTitle, 256) | Out-Null
$title = $windowTitle.ToString()

if ($title -like '*DaVinci Resolve*') {
    Write-Output "FOCUSED:$title"
} else {
    Write-Output "NOT_FOCUSED:$title"
}
"""

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = result.stdout.strip()
        if output.startswith("FOCUSED:"):
            return {"focused": True, "current_window": output.replace("FOCUSED:", "")}
        else:
            return {
                "focused": False,
                "current_window": output.replace("NOT_FOCUSED:", ""),
            }
    except Exception as e:
        return {"focused": False, "error": str(e)}


def send_key_if_focused(key: str, description: str = "") -> Dict[str, Any]:
    """
    Send a key to DaVinci Resolve ONLY if it's already focused.

    This is a non-intrusive mode that won't steal focus from the user's
    current work. Useful for automation that should only run when the user
    is actively working in Resolve.

    Args:
        key: The key to send in SendKeys format
        description: Optional description of the action

    Returns:
        Dict with success status and message
    """
    focus_check = is_resolve_focused()

    if focus_check.get("error"):
        return {"success": False, "error": focus_check["error"]}

    if not focus_check.get("focused"):
        current_window = focus_check.get("current_window", "unknown")
        return {
            "success": False,
            "error": f"DaVinci Resolve not focused (current: '{current_window}'). Use send_key_to_resolve() to force focus.",
            "skipped": True,
        }

    # Resolve is already focused, send key without re-focusing
    return send_key_to_resolve(key, description, verify_focus=True, retry_count=1)


def reset_resolve_context(escape_count: int = 3) -> Dict[str, Any]:
    """
    Reset DaVinci Resolve to a known state by pressing Escape multiple times.

    As per the WSL2 automation documentation: "the best recovery is to reset
    the context – e.g. pressing Esc a few times to close any open dialogs
    and bring Resolve to a known state".

    Args:
        escape_count: Number of Escape presses (default: 3)

    Returns:
        Dict with success status
    """
    logger.info(f"Resetting Resolve context with {escape_count} Escape presses")

    for i in range(escape_count):
        result = send_key_to_resolve(
            "{ESC}", f"Reset context (Escape {i + 1}/{escape_count})"
        )
        if not result.get("success"):
            return {
                "success": False,
                "error": f"Failed on Escape {i + 1}: {result.get('error')}",
            }

    return {
        "success": True,
        "message": f"Sent {escape_count} Escape keys to reset context",
    }


def send_custom_key(key: str, description: str = "custom key") -> Dict[str, Any]:
    """
    Send a custom key combination to DaVinci Resolve.

    Args:
        key: The key in SendKeys format
            - Regular keys: 'a', 'b', '1', etc.
            - Special keys: {ENTER}, {TAB}, {ESC}, {BACKSPACE}, {DELETE}
            - Arrow keys: {LEFT}, {RIGHT}, {UP}, {DOWN}
            - Function keys: {F1} through {F12}
            - Modifiers: ^ for Ctrl, + for Shift, % for Alt
            - Examples: '^s' (Ctrl+S), '+{F10}' (Shift+F10), '%{F4}' (Alt+F4)
        description: Optional description of the action

    Returns:
        Dict with success status and message
    """
    return send_key_to_resolve(key, description)
