#!/usr/bin/env python3
"""
DaVinci Resolve Sync Operations
Audio sync, linking and relinking clips
"""

import logging
from typing import List

from .pool import get_all_media_pool_clips

logger = logging.getLogger("davinci-resolve-mcp.media.sync")


def auto_sync_audio(
    resolve,
    clip_names: List[str],
    sync_method: str = "waveform",
    append_mode: bool = False,
    target_bin: str = None,
) -> str:
    """Sync audio between clips with customizable settings."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not clip_names or len(clip_names) < 2:
        return "Error: At least two clips are required for audio synchronization"

    if sync_method not in ["waveform", "timecode"]:
        return "Error: Sync method must be 'waveform' or 'timecode'"

    result = get_all_media_pool_clips(resolve)
    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    all_clips = result["clips"]
    root_folder = result["root_folder"]
    folders = result["folders"]
    media_pool = result["media_pool"]

    # Find clips by name
    clips_to_sync = []
    for name in clip_names:
        found = False
        for clip in all_clips:
            if clip and clip.GetName() == name:
                clips_to_sync.append(clip)
                found = True
                break
        if not found:
            return f"Error: Clip '{name}' not found in Media Pool"

    try:
        set_result = media_pool.SetCurrentFolder(root_folder)
        if not set_result:
            return "Error: Failed to set current folder to root"

        select_result = media_pool.SelectClips(clips_to_sync)
        if not select_result:
            return "Error: Failed to select clips for syncing"

        sync_options = {
            "syncMethod": 0 if sync_method == "waveform" else 1,
            "appendMode": append_mode,
        }

        sync_result = media_pool.AutoSyncAudio(sync_options)

        if not sync_result:
            return "Error: Failed to sync audio for the selected clips"

        if target_bin:
            target_folder = None

            if target_bin.lower() == "master" or target_bin == root_folder.GetName():
                target_folder = root_folder
            else:
                for folder in folders:
                    if folder and folder.GetName() == target_bin:
                        target_folder = folder
                        break

            if not target_folder:
                return f"Warning: Synced clips but bin '{target_bin}' not found for moving clips"

            move_result = media_pool.MoveClips(clips_to_sync, target_folder)
            if not move_result:
                return f"Warning: Synced clips but failed to move them to bin '{target_bin}'"

        return f"Successfully synced audio for {len(clips_to_sync)} clips using {sync_method} method"

    except Exception as e:
        return f"Error syncing audio: {str(e)}"


def unlink_clips(resolve, clip_names: List[str]) -> str:
    """Unlink specified clips, disconnecting them from their media files."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not clip_names or len(clip_names) == 0:
        return "Error: No clip names provided for unlinking"

    result = get_all_media_pool_clips(resolve)
    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    all_clips = result["clips"]
    media_pool = result["media_pool"]

    clips_to_unlink = []
    not_found_clips = []

    for name in clip_names:
        found = False
        for clip in all_clips:
            if clip and clip.GetName() == name:
                clips_to_unlink.append(clip)
                found = True
                break
        if not found:
            not_found_clips.append(name)

    if not_found_clips:
        return f"Error: Clips not found in Media Pool: {', '.join(not_found_clips)}"

    if not clips_to_unlink:
        return "Error: No valid clips found to unlink"

    try:
        unlink_result = media_pool.UnlinkClips(clips_to_unlink)

        if unlink_result:
            return f"Successfully unlinked {len(clips_to_unlink)} clips"
        else:
            return "Error: Failed to unlink clips"

    except Exception as e:
        return f"Error unlinking clips: {str(e)}"


def relink_clips(
    resolve,
    clip_names: List[str],
    media_paths: List[str] = None,
    folder_path: str = None,
    recursive: bool = False,
) -> str:
    """Relink specified clips to their media files."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not clip_names or len(clip_names) == 0:
        return "Error: No clip names provided for relinking"

    if media_paths is None and folder_path is None:
        return "Error: Either media_paths or folder_path must be provided for relinking"

    if media_paths is not None and folder_path is not None:
        return "Error: Cannot specify both media_paths and folder_path, choose one approach"

    if (
        media_paths is not None
        and len(media_paths) > 0
        and len(media_paths) != len(clip_names)
    ):
        return "Error: If providing media_paths, the number must match the number of clip_names"

    result = get_all_media_pool_clips(resolve)
    if isinstance(result, dict) and "error" in result:
        return f"Error: {result['error']}"

    all_clips = result["clips"]
    media_pool = result["media_pool"]

    clips_to_relink = []
    not_found_clips = []

    for name in clip_names:
        found = False
        for clip in all_clips:
            if clip and clip.GetName() == name:
                clips_to_relink.append(clip)
                found = True
                break
        if not found:
            not_found_clips.append(name)

    if not_found_clips:
        return f"Error: Clips not found in Media Pool: {', '.join(not_found_clips)}"

    if not clips_to_relink:
        return "Error: No valid clips found to relink"

    try:
        relink_result = False

        if media_paths:
            relink_result = media_pool.RelinkClips(clips_to_relink, media_paths)
        else:
            relink_options = {"recursive": recursive}
            relink_result = media_pool.RelinkClips(
                clips_to_relink, [], folder_path, relink_options
            )

        if relink_result:
            if media_paths:
                return f"Successfully relinked {len(clips_to_relink)} clips to specified media paths"
            else:
                return f"Successfully relinked {len(clips_to_relink)} clips using media from {folder_path}"
        else:
            if media_paths:
                return "Error: Failed to relink clips to specified media paths"
            else:
                return f"Error: Failed to relink clips using media from {folder_path}"

    except Exception as e:
        return f"Error relinking clips: {str(e)}"
