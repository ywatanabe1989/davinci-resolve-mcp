#!/usr/bin/env python3
"""Marker operation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def marker_add() -> Dict[str, Any]:
    """Add marker at playhead (M)."""
    return send_key_to_resolve("m", "Add Marker (M)")


def marker_add_and_modify() -> Dict[str, Any]:
    """Add marker and open modify dialog (Ctrl+M)."""
    return send_key_to_resolve("^m", "Add/Modify Marker (Ctrl+M)")


def marker_modify() -> Dict[str, Any]:
    """Modify existing marker (Shift+M)."""
    return send_key_to_resolve("+m", "Modify Marker (Shift+M)")


def marker_delete() -> Dict[str, Any]:
    """Delete marker at playhead (Alt+M)."""
    return send_key_to_resolve("%m", "Delete Marker (Alt+M)")


def marker_go_to_next() -> Dict[str, Any]:
    """Go to next marker (Shift+Down)."""
    return send_key_to_resolve("+{DOWN}", "Next Marker (Shift+Down)")


def marker_go_to_previous() -> Dict[str, Any]:
    """Go to previous marker (Shift+Up)."""
    return send_key_to_resolve("+{UP}", "Previous Marker (Shift+Up)")
