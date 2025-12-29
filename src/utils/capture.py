"""
Screenshot Capture Utilities for DaVinci Resolve MCP Server.

Provides portable screenshot functionality for AI agents to "see" DaVinci Resolve.
Optimized for WSL-to-Windows capture. Lightweight, standalone implementation.
"""

import os
import sys
import subprocess
import base64
from datetime import datetime
from typing import Optional, Dict, Any

# Default output directory
DEFAULT_OUTPUT_DIR = os.path.expanduser("~/.scitex/capture")


def is_wsl() -> bool:
    """Check if running in WSL."""
    return sys.platform == "linux" and "microsoft" in os.uname().release.lower()


def find_powershell() -> Optional[str]:
    """Find PowerShell executable."""
    ps_paths = [
        "powershell.exe",
        "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        "/mnt/c/Windows/SysWOW64/WindowsPowerShell/v1.0/powershell.exe",
    ]

    for path in ps_paths:
        try:
            result = subprocess.run(
                [path, "-Command", "echo test"],
                capture_output=True,
                timeout=2,
            )
            if result.returncode == 0:
                return path
        except Exception:
            continue
    return None


def _run_powershell(script: str, timeout: int = 10) -> tuple:
    """Run PowerShell script and return (success, output, error)."""
    ps_exe = find_powershell()
    if not ps_exe:
        return False, None, "PowerShell not found"

    try:
        result = subprocess.run(
            [ps_exe, "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip(), None
        return False, None, result.stderr or "Command failed"
    except subprocess.TimeoutExpired:
        return False, None, "Timeout"
    except Exception as e:
        return False, None, str(e)


def _save_image(png_data: bytes, output_path: str, quality: int) -> str:
    """Save PNG data to file, converting to JPEG if PIL available."""
    try:
        import io
        from PIL import Image

        img = Image.open(io.BytesIO(png_data))
        if img.mode == "RGBA":
            rgb_img = Image.new("RGB", img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        return output_path
    except ImportError:
        output_path = output_path.replace(".jpg", ".png")
        with open(output_path, "wb") as f:
            f.write(png_data)
        return output_path


def capture_screenshot(
    output_path: str = None,
    quality: int = 85,
    monitor_id: int = 0,
    capture_all: bool = False,
    return_base64: bool = False,
) -> Dict[str, Any]:
    """
    Take a screenshot of the Windows desktop from WSL.

    Args:
        output_path: Path to save screenshot (auto-generated if None)
        quality: JPEG quality (1-100)
        monitor_id: Monitor index (0-based)
        capture_all: Capture all monitors combined
        return_base64: Return image as base64 string instead of saving

    Returns:
        Dict with 'success', 'path' or 'base64', and optional 'error'
    """
    if not is_wsl():
        return {"success": False, "error": "Not running in WSL"}

    # Build capture script
    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    Add-Type @'
    using System;
    using System.Runtime.InteropServices;
    public class User32 { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); }
'@
    $null = [User32]::SetProcessDPIAware()
    $screens = [System.Windows.Forms.Screen]::AllScreens
    """

    if capture_all:
        ps_script += """
    $minX = ($screens | ForEach-Object { $_.Bounds.X } | Measure-Object -Minimum).Minimum
    $minY = ($screens | ForEach-Object { $_.Bounds.Y } | Measure-Object -Minimum).Minimum
    $maxX = ($screens | ForEach-Object { $_.Bounds.X + $_.Bounds.Width } | Measure-Object -Maximum).Maximum
    $maxY = ($screens | ForEach-Object { $_.Bounds.Y + $_.Bounds.Height } | Measure-Object -Maximum).Maximum
    $bitmap = New-Object System.Drawing.Bitmap ($maxX - $minX), ($maxY - $minY)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($minX, $minY, 0, 0, [System.Drawing.Size]::new(($maxX - $minX), ($maxY - $minY)))
    """
    else:
        ps_script += f"""
    $idx = {monitor_id}; if ($idx -ge $screens.Count) {{ $idx = 0 }}
    $screen = $screens[$idx]
    $bitmap = New-Object System.Drawing.Bitmap $screen.Bounds.Width, $screen.Bounds.Height
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Bounds.X, $screen.Bounds.Y, 0, 0, $bitmap.Size)
    """

    ps_script += """
    $stream = New-Object System.IO.MemoryStream
    $bitmap.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
    [Convert]::ToBase64String($stream.ToArray())
    $graphics.Dispose(); $bitmap.Dispose(); $stream.Dispose()
    """

    success, output, error = _run_powershell(ps_script)
    if not success:
        return {"success": False, "error": error}

    if return_base64:
        return {"success": True, "base64": output, "format": "png"}

    png_data = base64.b64decode(output)

    if output_path is None:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{DEFAULT_OUTPUT_DIR}/screenshot_{timestamp}.jpg"

    saved_path = _save_image(png_data, output_path, quality)
    return {"success": True, "path": saved_path}


def list_windows() -> Dict[str, Any]:
    """List all visible windows with their handles."""
    if not is_wsl():
        return {"success": False, "error": "Not running in WSL"}

    ps_script = """
    Add-Type @'
    using System; using System.Runtime.InteropServices; using System.Text; using System.Collections.Generic;
    public class WinEnum {
        [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
        [DllImport("user32.dll")] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
        [DllImport("user32.dll")] static extern int GetWindowTextLength(IntPtr h);
        [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
        public delegate bool EnumProc(IntPtr h, IntPtr l);
        [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc e, IntPtr l);
        public static List<object[]> Get() {
            var w = new List<object[]>();
            EnumWindows((h, l) => {
                if (IsWindowVisible(h)) { int len = GetWindowTextLength(h);
                    if (len > 0) { var sb = new StringBuilder(len + 1); GetWindowText(h, sb, sb.Capacity);
                        uint p; GetWindowThreadProcessId(h, out p); w.Add(new object[] { h.ToInt64(), sb.ToString(), p }); }
                } return true; }, IntPtr.Zero);
            return w; } }
'@
    $r = @(); foreach ($w in [WinEnum]::Get()) {
        $p = Get-Process -Id $w[2] -ErrorAction SilentlyContinue
        $r += @{ Handle = $w[0]; Title = $w[1]; ProcessName = if ($p) { $p.ProcessName } else { "Unknown" } }
    }; $r | ConvertTo-Json -Compress
    """

    success, output, error = _run_powershell(ps_script)
    if not success:
        return {"success": False, "error": error}

    import json

    windows = json.loads(output)
    if isinstance(windows, dict):
        windows = [windows]
    return {"success": True, "windows": windows}


def capture_window(
    window_handle: int,
    output_path: str = None,
    quality: int = 85,
    return_base64: bool = False,
) -> Dict[str, Any]:
    """Capture a specific window by its handle."""
    if not is_wsl():
        return {"success": False, "error": "Not running in WSL"}

    ps_script = f"""
    Add-Type -AssemblyName System.Drawing
    Add-Type @'
    using System; using System.Drawing; using System.Runtime.InteropServices;
    public class WinCap {{
        [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
        [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
        [StructLayout(LayoutKind.Sequential)] public struct RECT {{ public int L, T, R, B; }}
        public static Bitmap Cap(IntPtr h) {{ SetProcessDPIAware(); RECT r; GetWindowRect(h, out r);
            int w = r.R - r.L, ht = r.B - r.T; if (w <= 0 || ht <= 0) return null;
            var b = new Bitmap(w, ht); using (var g = Graphics.FromImage(b)) {{ g.CopyFromScreen(r.L, r.T, 0, 0, new Size(w, ht)); }}
            return b; }} }}
'@
    $b = [WinCap]::Cap([IntPtr]{window_handle}); if ($b -eq $null) {{ exit 1 }}
    $s = New-Object System.IO.MemoryStream; $b.Save($s, [System.Drawing.Imaging.ImageFormat]::Png)
    [Convert]::ToBase64String($s.ToArray()); $b.Dispose(); $s.Dispose()
    """

    success, output, error = _run_powershell(ps_script)
    if not success:
        return {"success": False, "error": error or "Window capture failed"}

    if return_base64:
        return {"success": True, "base64": output, "format": "png"}

    png_data = base64.b64decode(output)

    if output_path is None:
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{DEFAULT_OUTPUT_DIR}/window_{window_handle}_{timestamp}.jpg"

    saved_path = _save_image(png_data, output_path, quality)
    return {"success": True, "path": saved_path}


def find_resolve_window() -> Optional[Dict[str, Any]]:
    """Find DaVinci Resolve window handle."""
    result = list_windows()
    if not result.get("success"):
        return None

    for window in result.get("windows", []):
        title = window.get("Title", "").lower()
        process = window.get("ProcessName", "").lower()
        if "davinci resolve" in title or process == "resolve":
            return window
    return None


def capture_resolve_window(
    output_path: str = None, quality: int = 85, return_base64: bool = False
) -> Dict[str, Any]:
    """Capture the DaVinci Resolve window."""
    window = find_resolve_window()
    if not window:
        return {"success": False, "error": "DaVinci Resolve window not found"}

    result = capture_window(window["Handle"], output_path, quality, return_base64)
    if result.get("success"):
        result["window_title"] = window.get("Title")
    return result


def get_monitor_info() -> Dict[str, Any]:
    """Get information about all monitors."""
    if not is_wsl():
        return {"success": False, "error": "Not running in WSL"}

    ps_script = """
    Add-Type -AssemblyName System.Windows.Forms
    $m = @(); $i = 0; foreach ($s in [System.Windows.Forms.Screen]::AllScreens) {
        $m += @{ Index = $i; DeviceName = $s.DeviceName; Primary = $s.Primary;
            Width = $s.Bounds.Width; Height = $s.Bounds.Height; X = $s.Bounds.X; Y = $s.Bounds.Y }; $i++ }
    @{ Monitors = $m; Count = $m.Count } | ConvertTo-Json -Compress
    """

    success, output, error = _run_powershell(ps_script)
    if not success:
        return {"success": False, "error": error}

    import json

    return {"success": True, **json.loads(output)}
