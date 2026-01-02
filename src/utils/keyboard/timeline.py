#!/usr/bin/env python3
"""Timeline navigation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def timeline_previous_clip() -> Dict[str, Any]:
    """Go to previous clip (Up Arrow)."""
    return send_key_to_resolve("{UP}", "Previous Clip (Up Arrow)")


def timeline_next_clip() -> Dict[str, Any]:
    """Go to next clip (Down Arrow)."""
    return send_key_to_resolve("{DOWN}", "Next Clip (Down Arrow)")


def timeline_step_1_second_forward() -> Dict[str, Any]:
    """Step forward 1 second (Shift+Right)."""
    return send_key_to_resolve("+{RIGHT}", "Step 1 Second Forward (Shift+Right)")


def timeline_step_1_second_backward() -> Dict[str, Any]:
    """Step backward 1 second (Shift+Left)."""
    return send_key_to_resolve("+{LEFT}", "Step 1 Second Backward (Shift+Left)")


def timeline_go_to_first_frame() -> Dict[str, Any]:
    """Go to first frame of clip (;)."""
    return send_key_to_resolve(";", "First Frame (;)")


def timeline_go_to_last_frame() -> Dict[str, Any]:
    """Go to last frame of clip (')."""
    return send_key_to_resolve("'", "Last Frame (')")


def timeline_go_to_prev_keyframe() -> Dict[str, Any]:
    """Go to previous keyframe ([)."""
    return send_key_to_resolve("[", "Previous Keyframe ([)")


def timeline_go_to_next_keyframe() -> Dict[str, Any]:
    """Go to next keyframe (])."""
    return send_key_to_resolve("]", "Next Keyframe (])")
