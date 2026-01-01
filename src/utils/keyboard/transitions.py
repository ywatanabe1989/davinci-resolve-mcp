#!/usr/bin/env python3
"""Transition functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def transition_add() -> Dict[str, Any]:
    """Add default transition (Ctrl+T)."""
    return send_key_to_resolve("^t", "Add Transition (Ctrl+T)")


def transition_add_video() -> Dict[str, Any]:
    """Add video transition only (Alt+T)."""
    return send_key_to_resolve("%t", "Add Video Transition (Alt+T)")


def transition_add_audio() -> Dict[str, Any]:
    """Add audio transition only (Shift+T)."""
    return send_key_to_resolve("+t", "Add Audio Transition (Shift+T)")
