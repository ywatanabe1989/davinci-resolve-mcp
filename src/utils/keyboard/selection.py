#!/usr/bin/env python3
"""Selection operation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def select_all() -> Dict[str, Any]:
    """Select all clips (Ctrl+A)."""
    return send_key_to_resolve("^a", "Select All (Ctrl+A)")


def deselect_all() -> Dict[str, Any]:
    """Deselect all clips (Ctrl+Shift+A)."""
    return send_key_to_resolve("^+a", "Deselect All (Ctrl+Shift+A)")


def select_clips_forward() -> Dict[str, Any]:
    """Select clips forward from playhead (Y)."""
    return send_key_to_resolve("y", "Select Clips Forward (Y)")


def select_clips_backward() -> Dict[str, Any]:
    """Select clips backward from playhead (Ctrl+Y)."""
    return send_key_to_resolve("^y", "Select Clips Backward (Ctrl+Y)")


def select_nearest_edit() -> Dict[str, Any]:
    """Select nearest edit point (V)."""
    return send_key_to_resolve("v", "Select Nearest Edit (V)")
