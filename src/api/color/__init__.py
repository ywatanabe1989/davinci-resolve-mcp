#!/usr/bin/env python3
"""
DaVinci Resolve Color Operations - Split Module
Re-exports all functions from submodules for backward compatibility.
"""

from .nodes import (
    get_current_node,
    add_node,
    ensure_clip_selected,
)

from .grades import (
    apply_lut,
    copy_grade,
)

from .wheels import (
    get_color_wheels,
    set_color_wheel_param,
)

__all__ = [
    # Node operations
    "get_current_node",
    "add_node",
    "ensure_clip_selected",
    # Grade operations
    "apply_lut",
    "copy_grade",
    # Wheel operations
    "get_color_wheels",
    "set_color_wheel_param",
]
