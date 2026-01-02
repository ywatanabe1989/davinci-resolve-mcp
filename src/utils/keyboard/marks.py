#!/usr/bin/env python3
"""Mark in/out operation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def mark_set_in() -> Dict[str, Any]:
    """Set mark in point at playhead (I)."""
    return send_key_to_resolve("i", "Set Mark In (I)")


def mark_set_out() -> Dict[str, Any]:
    """Set mark out point at playhead (O)."""
    return send_key_to_resolve("o", "Set Mark Out (O)")


def mark_clip() -> Dict[str, Any]:
    """Mark the current clip (X)."""
    return send_key_to_resolve("x", "Mark Clip (X)")


def mark_go_to_in() -> Dict[str, Any]:
    """Go to mark in point (Shift+I)."""
    return send_key_to_resolve("+i", "Go to Mark In (Shift+I)")


def mark_go_to_out() -> Dict[str, Any]:
    """Go to mark out point (Shift+O)."""
    return send_key_to_resolve("+o", "Go to Mark Out (Shift+O)")


def mark_clear_in() -> Dict[str, Any]:
    """Clear mark in point (Alt+I)."""
    return send_key_to_resolve("%i", "Clear Mark In (Alt+I)")


def mark_clear_out() -> Dict[str, Any]:
    """Clear mark out point (Alt+O)."""
    return send_key_to_resolve("%o", "Clear Mark Out (Alt+O)")


def mark_clear_both() -> Dict[str, Any]:
    """Clear both mark in and out (Alt+X)."""
    return send_key_to_resolve("%x", "Clear Mark In/Out (Alt+X)")
