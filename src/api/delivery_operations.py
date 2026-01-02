#!/usr/bin/env python3
"""
DaVinci Resolve Delivery Page Operations
Re-exports from split submodules for backward compatibility.
"""

# Re-export all functions from submodules
from src.api.delivery.render import (
    get_render_presets,
    add_to_render_queue,
    validate_render_preset,
)

from src.api.delivery.queue import (
    start_render,
    get_render_queue_status,
    clear_render_queue,
)

__all__ = [
    # Render operations
    "get_render_presets",
    "add_to_render_queue",
    "validate_render_preset",
    # Queue operations
    "start_render",
    "get_render_queue_status",
    "clear_render_queue",
]
