#!/usr/bin/env python3
"""Playback control functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def playback_play_pause() -> Dict[str, Any]:
    """Toggle play/pause in DaVinci Resolve."""
    return send_key_to_resolve(" ", "Play/Pause (Space)")


def playback_stop() -> Dict[str, Any]:
    """Stop playback in DaVinci Resolve."""
    return send_key_to_resolve("k", "Stop (K)")


def playback_forward() -> Dict[str, Any]:
    """Play forward (L key - press multiple times for faster)."""
    return send_key_to_resolve("l", "Play Forward (L)")


def playback_reverse() -> Dict[str, Any]:
    """Play in reverse (J key - press multiple times for faster)."""
    return send_key_to_resolve("j", "Play Reverse (J)")


def playback_step_forward() -> Dict[str, Any]:
    """Step forward one frame."""
    return send_key_to_resolve("{RIGHT}", "Step Forward (Right Arrow)")


def playback_step_backward() -> Dict[str, Any]:
    """Step backward one frame."""
    return send_key_to_resolve("{LEFT}", "Step Backward (Left Arrow)")


def playback_go_to_start() -> Dict[str, Any]:
    """Go to the start of the timeline."""
    return send_key_to_resolve("{HOME}", "Go to Start (Home)")


def playback_go_to_end() -> Dict[str, Any]:
    """Go to the end of the timeline."""
    return send_key_to_resolve("{END}", "Go to End (End)")


def playback_loop_toggle() -> Dict[str, Any]:
    """Toggle loop playback mode."""
    return send_key_to_resolve("^/", "Toggle Loop (Ctrl+/)")


def playback_fast_forward() -> Dict[str, Any]:
    """Fast forward (Shift+L)."""
    return send_key_to_resolve("+l", "Fast Forward (Shift+L)")


def playback_fast_reverse() -> Dict[str, Any]:
    """Fast reverse (Shift+J)."""
    return send_key_to_resolve("+j", "Fast Reverse (Shift+J)")


def playback_play_around() -> Dict[str, Any]:
    """Play around current position (/)."""
    return send_key_to_resolve("/", "Play Around (/)")
