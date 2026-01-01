#!/usr/bin/env python3
"""Retime control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def retime_controls() -> Dict[str, Any]:
    """Show retime controls (Ctrl+R)."""
    return send_key_to_resolve("^r", "Retime Controls (Ctrl+R)")


def retime_freeze_frame() -> Dict[str, Any]:
    """Create freeze frame (Shift+R)."""
    return send_key_to_resolve("+r", "Freeze Frame (Shift+R)")
