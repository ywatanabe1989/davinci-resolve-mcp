#!/usr/bin/env python3
"""
DaVinci Resolve Media Pool Operations
Basic media pool management: listing, importing, bins
"""

import logging
import os
from typing import List, Dict, Any

logger = logging.getLogger("davinci-resolve-mcp.media.pool")


def get_all_media_pool_clips(resolve):
    """Helper to get all clips from media pool (root and subfolders).

    Returns:
        Tuple of (all_clips, root_folder, folders, media_pool) or error dict
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return {"error": "Failed to get Media Pool"}

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return {"error": "Failed to get Root Folder"}

    all_clips = []

    root_clips = root_folder.GetClipList()
    if root_clips:
        all_clips.extend(root_clips)

    folders = root_folder.GetSubFolderList()
    for folder in folders:
        if folder:
            folder_clips = folder.GetClipList()
            if folder_clips:
                all_clips.extend(folder_clips)

    return {
        "clips": all_clips,
        "root_folder": root_folder,
        "folders": folders,
        "media_pool": media_pool,
    }


def list_media_pool_clips(resolve) -> List[Dict[str, Any]]:
    """List all clips in the media pool of the current project."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return [{"error": "No project currently open"}]

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return [{"error": "Failed to get Media Pool"}]

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return [{"error": "Failed to get Root Folder"}]

    clips = root_folder.GetClipList()

    clip_info = []
    for clip in clips:
        if clip:
            clip_info.append(
                {
                    "name": clip.GetName(),
                    "type": clip.GetClipProperty()["Type"],
                    "duration": clip.GetClipProperty()["Duration"],
                    "fps": clip.GetClipProperty().get("FPS", "Unknown"),
                }
            )

    return clip_info if clip_info else [{"info": "No clips found in the media pool"}]


def import_media(resolve, file_path: str) -> str:
    """Import a media file into the current project's media pool."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not file_path:
        return "Error: File path cannot be empty"

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return "Error: Failed to get Media Pool"

    imported_media = media_pool.ImportMedia([file_path])

    if imported_media and len(imported_media) > 0:
        return f"Successfully imported '{os.path.basename(file_path)}'"
    else:
        return (
            f"Failed to import '{file_path}'. The file may be in an unsupported format."
        )


def create_bin(resolve, name: str) -> str:
    """Create a new bin/folder in the media pool."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not name:
        return "Error: Bin name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return "Error: Failed to get Media Pool"

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return "Error: Failed to get Root Folder"

    folders = root_folder.GetSubFolderList()
    for folder in folders:
        if folder.GetName() == name:
            return f"Error: Bin '{name}' already exists"

    new_bin = media_pool.AddSubFolder(root_folder, name)

    if new_bin:
        return f"Successfully created bin '{name}'"
    else:
        return f"Failed to create bin '{name}'"


def list_bins(resolve) -> List[Dict[str, Any]]:
    """List all bins/folders in the media pool of the current project."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return [{"error": "No project currently open"}]

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return [{"error": "Failed to get Media Pool"}]

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return [{"error": "Failed to get Root Folder"}]

    folders = root_folder.GetSubFolderList()

    bin_info = []
    bin_info.append(
        {
            "name": root_folder.GetName() or "Master",
            "is_root": True,
            "clip_count": len(root_folder.GetClipList()),
        }
    )

    for folder in folders:
        if folder:
            bin_info.append(
                {
                    "name": folder.GetName(),
                    "is_root": False,
                    "clip_count": len(folder.GetClipList()),
                }
            )

    return (
        bin_info if len(bin_info) > 1 else [{"info": "No bins found in the media pool"}]
    )


def get_bin_contents(resolve, bin_name: str) -> List[Dict[str, Any]]:
    """Get the contents of a specific bin/folder in the media pool."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return [{"error": "No project currently open"}]

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return [{"error": "Failed to get Media Pool"}]

    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        return [{"error": "Failed to get Root Folder"}]

    if bin_name.lower() == "master" or bin_name == root_folder.GetName():
        clips = root_folder.GetClipList()
        return format_clip_list(clips, "Master")

    folders = root_folder.GetSubFolderList()
    target_folder = None

    for folder in folders:
        if folder and folder.GetName() == bin_name:
            target_folder = folder
            break

    if not target_folder:
        return [{"error": f"Bin '{bin_name}' not found in Media Pool"}]

    clips = target_folder.GetClipList()
    return format_clip_list(clips, bin_name)


def format_clip_list(clips, bin_name: str) -> List[Dict[str, Any]]:
    """Helper function to format clip info from a clip list."""
    if not clips:
        return [{"info": f"No clips found in bin '{bin_name}'"}]

    clip_info = []
    for clip in clips:
        if clip:
            properties = clip.GetClipProperty()
            clip_info.append(
                {
                    "name": clip.GetName(),
                    "type": properties.get("Type", "Unknown"),
                    "duration": properties.get("Duration", "Unknown"),
                    "fps": properties.get("FPS", "Unknown"),
                    "resolution": f"{properties.get('Width', '?')}x{properties.get('Height', '?')}",
                    "bin": bin_name,
                }
            )

    return clip_info
