#!/usr/bin/env python3
"""Viewer control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def viewer_toggle_source_timeline() -> Dict[str, Any]:
    """Toggle between source and timeline viewer (Q)."""
    return send_key_to_resolve("q", "Toggle Source/Timeline (Q)")


def viewer_match_frame() -> Dict[str, Any]:
    """Match frame (F)."""
    return send_key_to_resolve("f", "Match Frame (F)")
