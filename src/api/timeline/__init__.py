#!/usr/bin/env python3
"""
DaVinci Resolve Timeline Operations - Split Module
Re-exports all functions from submodules for backward compatibility.
"""

from .basic import (
    list_timelines,
    get_current_timeline_info,
    create_timeline,
    create_empty_timeline,
    set_current_timeline,
    delete_timeline,
    get_timeline_tracks,
)

from .markers import (
    add_marker,
)

__all__ = [
    # Basic timeline operations
    "list_timelines",
    "get_current_timeline_info",
    "create_timeline",
    "create_empty_timeline",
    "set_current_timeline",
    "delete_timeline",
    "get_timeline_tracks",
    # Marker operations
    "add_marker",
]
