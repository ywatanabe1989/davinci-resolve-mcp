#!/usr/bin/env python3
"""Color page specific functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def color_grab_still() -> Dict[str, Any]:
    """Grab still from current frame (Ctrl+Alt+G)."""
    return send_key_to_resolve("^%g", "Grab Still (Ctrl+Alt+G)")


def color_auto_balance() -> Dict[str, Any]:
    """Auto color balance (Alt+A)."""
    return send_key_to_resolve("%a", "Auto Color (Alt+A)")


def color_highlight() -> Dict[str, Any]:
    """Toggle highlight mode (Shift+H)."""
    return send_key_to_resolve("+h", "Toggle Highlight (Shift+H)")


def color_add_version() -> Dict[str, Any]:
    """Add new version (Ctrl+Y)."""
    return send_key_to_resolve("^y", "Add Version (Ctrl+Y)")


def color_load_memory_a() -> Dict[str, Any]:
    """Load color memory A (Ctrl+1)."""
    return send_key_to_resolve("^1", "Load Memory A (Ctrl+1)")


def color_save_memory_a() -> Dict[str, Any]:
    """Save color memory A (Alt+1)."""
    return send_key_to_resolve("%1", "Save Memory A (Alt+1)")


def color_load_memory_b() -> Dict[str, Any]:
    """Load color memory B (Ctrl+2)."""
    return send_key_to_resolve("^2", "Load Memory B (Ctrl+2)")


def color_save_memory_b() -> Dict[str, Any]:
    """Save color memory B (Alt+2)."""
    return send_key_to_resolve("%2", "Save Memory B (Alt+2)")


def color_load_memory_c() -> Dict[str, Any]:
    """Load color memory C (Ctrl+3)."""
    return send_key_to_resolve("^3", "Load Memory C (Ctrl+3)")


def color_save_memory_c() -> Dict[str, Any]:
    """Save color memory C (Alt+3)."""
    return send_key_to_resolve("%3", "Save Memory C (Alt+3)")


def color_load_memory_d() -> Dict[str, Any]:
    """Load color memory D (Ctrl+4)."""
    return send_key_to_resolve("^4", "Load Memory D (Ctrl+4)")


def color_save_memory_d() -> Dict[str, Any]:
    """Save color memory D (Alt+4)."""
    return send_key_to_resolve("%4", "Save Memory D (Alt+4)")


def color_apply_grade_from_one_prior() -> Dict[str, Any]:
    """Apply grade from one clip prior (=)."""
    return send_key_to_resolve("=", "Apply Grade One Prior (=)")


def color_apply_grade_from_two_prior() -> Dict[str, Any]:
    """Apply grade from two clips prior (-)."""
    return send_key_to_resolve("-", "Apply Grade Two Prior (-)")
