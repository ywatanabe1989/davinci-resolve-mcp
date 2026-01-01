#!/usr/bin/env python3
"""Clip control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def clip_enable_disable() -> Dict[str, Any]:
    """Enable/Disable selected clip (D)."""
    return send_key_to_resolve("d", "Enable/Disable Clip (D)")


def clip_create_subclip() -> Dict[str, Any]:
    """Create subclip from selection (Alt+B)."""
    return send_key_to_resolve("%b", "Create Subclip (Alt+B)")


def clip_add_flag() -> Dict[str, Any]:
    """Add flag to clip (G)."""
    return send_key_to_resolve("g", "Add Flag (G)")


def clip_change_duration() -> Dict[str, Any]:
    """Change clip duration dialog (Ctrl+D)."""
    return send_key_to_resolve("^d", "Change Clip Duration (Ctrl+D)")
