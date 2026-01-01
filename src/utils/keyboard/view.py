#!/usr/bin/env python3
"""View control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def view_zoom_in() -> Dict[str, Any]:
    """Zoom in on timeline (Ctrl+=)."""
    return send_key_to_resolve("^=", "Zoom In (Ctrl+=)")


def view_zoom_out() -> Dict[str, Any]:
    """Zoom out on timeline (Ctrl+-)."""
    return send_key_to_resolve("^-", "Zoom Out (Ctrl+-)")


def view_zoom_in_viewer() -> Dict[str, Any]:
    """Zoom in on viewer (+)."""
    return send_key_to_resolve("{ADD}", "Zoom In Viewer (+)")


def view_zoom_out_viewer() -> Dict[str, Any]:
    """Zoom out on viewer (-)."""
    return send_key_to_resolve("{SUBTRACT}", "Zoom Out Viewer (-)")


def view_fit_timeline() -> Dict[str, Any]:
    """Fit timeline to view (Shift+Z)."""
    return send_key_to_resolve("+z", "Fit Timeline (Shift+Z)")


def view_fullscreen_preview() -> Dict[str, Any]:
    """Toggle fullscreen preview (P)."""
    return send_key_to_resolve("p", "Fullscreen Preview (P)")


def view_fullscreen_viewer() -> Dict[str, Any]:
    """Toggle fullscreen viewer (Shift+F)."""
    return send_key_to_resolve("+f", "Fullscreen Viewer (Shift+F)")


def view_enhanced_viewer() -> Dict[str, Any]:
    """Toggle enhanced viewer (Alt+F)."""
    return send_key_to_resolve("%f", "Enhanced Viewer (Alt+F)")


def view_cinema_viewer() -> Dict[str, Any]:
    """Toggle cinema viewer (Ctrl+F)."""
    return send_key_to_resolve("^f", "Cinema Viewer (Ctrl+F)")


def view_expand_display() -> Dict[str, Any]:
    """Expand display (F4)."""
    return send_key_to_resolve("{F4}", "Expand Display (F4)")


def view_split_screen() -> Dict[str, Any]:
    """Toggle split screen (Ctrl+Alt+W)."""
    return send_key_to_resolve("^%w", "Split Screen (Ctrl+Alt+W)")


def view_video_scopes() -> Dict[str, Any]:
    """Toggle video scopes (Ctrl+Shift+W)."""
    return send_key_to_resolve("^+w", "Video Scopes (Ctrl+Shift+W)")


def view_display_left() -> Dict[str, Any]:
    """Left display (1)."""
    return send_key_to_resolve("1", "Left Display (1)")


def view_display_right() -> Dict[str, Any]:
    """Right display (2)."""
    return send_key_to_resolve("2", "Right Display (2)")


def view_display_red_channel() -> Dict[str, Any]:
    """Display red channel only (R)."""
    return send_key_to_resolve("r", "Red Channel (R)")


def view_display_z_buffer() -> Dict[str, Any]:
    """Display Z buffer (Z)."""
    return send_key_to_resolve("z", "Z Buffer (Z)")


def view_display_full_color() -> Dict[str, Any]:
    """Display full color (C)."""
    return send_key_to_resolve("c", "Full Color (C)")
