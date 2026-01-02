#!/usr/bin/env python3
"""
Focus management for DaVinci Resolve MCP Server.

Provides functionality to save and restore user's window focus and cursor
position during UI automation operations. This ensures the user's context
is preserved when the AI performs operations on DaVinci Resolve.

Key features:
- Save current window handle and cursor position before operations
- Restore user's focus and cursor after operations complete
- Context manager for automatic save/restore around operations
- Decorator for wrapping functions with state preservation
"""

import subprocess
import logging
from typing import Dict, Any, Optional

from .core import get_platform_type

logger = logging.getLogger("davinci-resolve-mcp.focus")

# Global state for user context preservation
_saved_user_state: Optional[Dict[str, Any]] = None


def save_user_state() -> Dict[str, Any]:
    """
    Save the user's current window focus and cursor position.

    This should be called before performing UI operations on DaVinci Resolve
    to preserve the user's context for later restoration.

    Returns:
        Dict with saved state or error
    """
    global _saved_user_state

    platform_type = get_platform_type()
    if platform_type not in ["windows", "wsl"]:
        return {"success": False, "error": f"Not supported on {platform_type}"}

    ps_script = """
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class UserState {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT { public int X; public int Y; }
}
'@

$foreground = [UserState]::GetForegroundWindow()
$windowTitle = New-Object System.Text.StringBuilder 256
[UserState]::GetWindowText($foreground, $windowTitle, 256) | Out-Null
$title = $windowTitle.ToString()

$pos = New-Object UserState+POINT
[UserState]::GetCursorPos([ref]$pos) | Out-Null

Write-Output "HANDLE:$foreground"
Write-Output "TITLE:$title"
Write-Output "CURSOR:$($pos.X),$($pos.Y)"
"""

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = result.stdout.strip()

        state = {}
        for line in output.split("\n"):
            if line.startswith("HANDLE:"):
                state["window_handle"] = line.replace("HANDLE:", "").strip()
            elif line.startswith("TITLE:"):
                state["window_title"] = line.replace("TITLE:", "").strip()
            elif line.startswith("CURSOR:"):
                coords = line.replace("CURSOR:", "").strip().split(",")
                state["cursor_x"] = int(coords[0])
                state["cursor_y"] = int(coords[1])

        _saved_user_state = state
        logger.info(
            f"Saved user state: {state.get('window_title', 'unknown')} "
            f"at ({state.get('cursor_x')}, {state.get('cursor_y')})"
        )
        return {"success": True, "state": state}

    except Exception as e:
        return {"success": False, "error": str(e)}


def restore_user_state() -> Dict[str, Any]:
    """
    Restore the user's previously saved window focus and cursor position.

    This should be called after performing UI operations on DaVinci Resolve
    to return the user to their previous context.

    Returns:
        Dict with success status
    """
    global _saved_user_state

    if _saved_user_state is None:
        return {"success": False, "error": "No saved state to restore"}

    platform_type = get_platform_type()
    if platform_type not in ["windows", "wsl"]:
        return {"success": False, "error": f"Not supported on {platform_type}"}

    handle = _saved_user_state.get("window_handle")
    cursor_x = _saved_user_state.get("cursor_x")
    cursor_y = _saved_user_state.get("cursor_y")
    title = _saved_user_state.get("window_title", "unknown")

    ps_script = f"""
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class RestoreState {{
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
}}
'@

$handle = [IntPtr]{handle}
[RestoreState]::SetForegroundWindow($handle) | Out-Null
Start-Sleep -Milliseconds 100
[RestoreState]::SetCursorPos({cursor_x}, {cursor_y}) | Out-Null
Write-Output "RESTORED"
"""

    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if "RESTORED" in result.stdout:
            logger.info(f"Restored user state: {title} at ({cursor_x}, {cursor_y})")
            _saved_user_state = None  # Clear saved state
            return {
                "success": True,
                "message": f"Restored focus to '{title}' and cursor to ({cursor_x}, {cursor_y})",
            }
        else:
            return {"success": False, "error": result.stdout or result.stderr}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_saved_state() -> Optional[Dict[str, Any]]:
    """Get the currently saved user state, if any."""
    return _saved_user_state


def clear_saved_state() -> None:
    """Clear the saved user state without restoring it."""
    global _saved_user_state
    _saved_user_state = None


def with_user_state_preserved(func):
    """
    Decorator that saves and restores user state around a function.

    Usage:
        @with_user_state_preserved
        def my_resolve_operation():
            # This will run with user state saved before and restored after
            send_key_to_resolve(" ", "Play/Pause")
    """

    def wrapper(*args, **kwargs):
        save_result = save_user_state()
        if not save_result.get("success"):
            logger.warning(f"Failed to save user state: {save_result.get('error')}")

        try:
            result = func(*args, **kwargs)
            return result
        finally:
            restore_result = restore_user_state()
            if not restore_result.get("success"):
                logger.warning(
                    f"Failed to restore user state: {restore_result.get('error')}"
                )

    return wrapper


class ResolveUIContext:
    """
    Context manager for safe Resolve UI operations.

    Automatically saves user's current window focus and cursor position,
    performs the operations, then restores the user's state.

    Usage:
        with ResolveUIContext("Adding clip to timeline"):
            send_key_to_resolve("^v", "Paste")
            send_key_to_resolve("{ENTER}", "Confirm")

    Args:
        description: Description of the operation for logging
    """

    def __init__(self, description: str = "UI operation"):
        self.description = description
        self.save_result = None

    def __enter__(self):
        logger.info(f"Starting UI operation: {self.description}")
        self.save_result = save_user_state()
        if not self.save_result.get("success"):
            logger.warning(
                f"Failed to save user state: {self.save_result.get('error')}"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        restore_result = restore_user_state()
        if not restore_result.get("success"):
            logger.warning(
                f"Failed to restore user state: {restore_result.get('error')}"
            )
        else:
            logger.info(f"Completed UI operation: {self.description}")
        return False  # Don't suppress exceptions


def resolve_ui_operation(description: str = "UI operation"):
    """
    Factory function for ResolveUIContext.

    Usage:
        with resolve_ui_operation("Adding clip to timeline"):
            send_key_to_resolve("^v", "Paste")
    """
    return ResolveUIContext(description)
