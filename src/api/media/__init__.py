#!/usr/bin/env python3
"""
DaVinci Resolve Media Operations - Split Module
Re-exports all functions from submodules for backward compatibility.
"""

from .pool import (
    list_media_pool_clips,
    import_media,
    create_bin,
    list_bins,
    get_bin_contents,
    format_clip_list,
    get_all_media_pool_clips,
)

from .clips import (
    list_timeline_clips,
    add_clip_to_timeline,
    delete_media,
    move_media_to_bin,
    create_sub_clip,
)

from .sync import (
    auto_sync_audio,
    unlink_clips,
    relink_clips,
)

__all__ = [
    # Pool operations
    "list_media_pool_clips",
    "import_media",
    "create_bin",
    "list_bins",
    "get_bin_contents",
    "format_clip_list",
    "get_all_media_pool_clips",
    # Clip operations
    "list_timeline_clips",
    "add_clip_to_timeline",
    "delete_media",
    "move_media_to_bin",
    "create_sub_clip",
    # Sync operations
    "auto_sync_audio",
    "unlink_clips",
    "relink_clips",
]
