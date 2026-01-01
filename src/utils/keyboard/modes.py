#!/usr/bin/env python3
"""Edit mode functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def mode_selection() -> Dict[str, Any]:
    """Normal edit/selection mode (A)."""
    return send_key_to_resolve("a", "Selection Mode (A)")


def mode_blade() -> Dict[str, Any]:
    """Blade/Razor mode (B)."""
    return send_key_to_resolve("b", "Blade Mode (B)")


def mode_trim() -> Dict[str, Any]:
    """Trim mode (T)."""
    return send_key_to_resolve("t", "Trim Mode (T)")


def mode_dynamic_trim() -> Dict[str, Any]:
    """Dynamic trim mode (W)."""
    return send_key_to_resolve("w", "Dynamic Trim Mode (W)")


def mode_slip_slide() -> Dict[str, Any]:
    """Slip/Slide mode (S)."""
    return send_key_to_resolve("s", "Slip/Slide Mode (S)")


def mode_edit_point_type() -> Dict[str, Any]:
    """Cycle edit point type (U)."""
    return send_key_to_resolve("u", "Edit Point Type (U)")


def mode_hand_tool() -> Dict[str, Any]:
    """Toggle hand/selection tool (H)."""
    return send_key_to_resolve("h", "Hand Tool (H)")


def toggle_snapping() -> Dict[str, Any]:
    """Toggle snapping (N)."""
    return send_key_to_resolve("n", "Toggle Snapping (N)")


def toggle_audio_scrubbing() -> Dict[str, Any]:
    """Toggle audio scrubbing (Shift+S)."""
    return send_key_to_resolve("+s", "Audio Scrubbing (Shift+S)")
