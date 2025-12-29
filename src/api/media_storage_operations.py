"""
MediaStorage Operations for DaVinci Resolve MCP Server.

Implements MediaStorage APIs for accessing mounted volumes and filesystem.
"""

from typing import List, Dict, Any


def get_mounted_volumes(resolve) -> List[str]:
    """Get list of mounted volumes displayed in Resolve's Media Storage."""
    if resolve is None:
        return ["Error: Not connected to DaVinci Resolve"]

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return ["Error: Failed to get Media Storage"]

        volumes = media_storage.GetMountedVolumeList()
        return volumes if volumes else []
    except Exception as e:
        return [f"Error: {str(e)}"]


def get_subfolder_list(resolve, folder_path: str) -> List[str]:
    """Get list of subfolders in the given folder path.

    Args:
        folder_path: Absolute folder path to get subfolders from
    """
    if resolve is None:
        return ["Error: Not connected to DaVinci Resolve"]

    if not folder_path:
        return ["Error: Folder path cannot be empty"]

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return ["Error: Failed to get Media Storage"]

        subfolders = media_storage.GetSubFolderList(folder_path)
        return subfolders if subfolders else []
    except Exception as e:
        return [f"Error: {str(e)}"]


def get_file_list(resolve, folder_path: str) -> List[str]:
    """Get list of media files in the given folder path.

    Args:
        folder_path: Absolute folder path to get files from
    """
    if resolve is None:
        return ["Error: Not connected to DaVinci Resolve"]

    if not folder_path:
        return ["Error: Folder path cannot be empty"]

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return ["Error: Failed to get Media Storage"]

        files = media_storage.GetFileList(folder_path)
        return files if files else []
    except Exception as e:
        return [f"Error: {str(e)}"]


def reveal_in_storage(resolve, path: str) -> str:
    """Expand and display the given path in Resolve's Media Storage.

    Args:
        path: File or folder path to reveal
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not path:
        return "Error: Path cannot be empty"

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return "Error: Failed to get Media Storage"

        result = media_storage.RevealInStorage(path)
        if result:
            return f"Successfully revealed '{path}' in Media Storage"
        else:
            return f"Failed to reveal '{path}' in Media Storage"
    except Exception as e:
        return f"Error: {str(e)}"


def add_items_to_media_pool(resolve, paths: List[str]) -> Dict[str, Any]:
    """Add files/folders from Media Storage to current Media Pool folder.

    Args:
        paths: List of file or folder paths to add
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    if not paths:
        return {"error": "Paths list cannot be empty"}

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return {"error": "Failed to get Media Storage"}

        clips = media_storage.AddItemListToMediaPool(paths)
        if clips:
            return {
                "success": True,
                "clips_added": len(clips),
                "clip_names": [clip.GetName() for clip in clips if clip],
            }
        else:
            return {"error": "Failed to add items to Media Pool"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def add_items_with_options(resolve, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add files to Media Pool with specific in/out points.

    Args:
        items: List of dicts with 'media' (path), 'startFrame', 'endFrame'
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    if not items:
        return {"error": "Items list cannot be empty"}

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return {"error": "Failed to get Media Storage"}

        clips = media_storage.AddItemListToMediaPool(items)
        if clips:
            return {
                "success": True,
                "clips_added": len(clips),
                "clip_names": [clip.GetName() for clip in clips if clip],
            }
        else:
            return {"error": "Failed to add items to Media Pool"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def add_clip_mattes(
    resolve, clip_name: str, matte_paths: List[str], stereo_eye: str = None
) -> str:
    """Add matte files to a media pool clip.

    Args:
        clip_name: Name of the clip to add mattes to
        matte_paths: List of paths to matte files
        stereo_eye: Optional 'left' or 'right' for stereo clips
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not clip_name or not matte_paths:
        return "Error: Clip name and matte paths are required"

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return "Error: Failed to get Media Storage"

        # Get the project and find the clip
        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        # Find the clip
        target_clip = None
        root_folder = media_pool.GetRootFolder()

        def find_clip(folder):
            clips = folder.GetClipList()
            if clips:
                for clip in clips:
                    if clip.GetName() == clip_name:
                        return clip
            subfolders = folder.GetSubFolderList()
            for subfolder in subfolders:
                result = find_clip(subfolder)
                if result:
                    return result
            return None

        target_clip = find_clip(root_folder)
        if not target_clip:
            return f"Error: Clip '{clip_name}' not found"

        if stereo_eye:
            result = media_storage.AddClipMattesToMediaPool(
                target_clip, matte_paths, stereo_eye
            )
        else:
            result = media_storage.AddClipMattesToMediaPool(target_clip, matte_paths)

        if result:
            return (
                f"Successfully added {len(matte_paths)} matte(s) to clip '{clip_name}'"
            )
        else:
            return f"Failed to add mattes to clip '{clip_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def add_timeline_mattes(resolve, matte_paths: List[str]) -> Dict[str, Any]:
    """Add timeline mattes to current media pool folder.

    Args:
        matte_paths: List of paths to matte files
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    if not matte_paths:
        return {"error": "Matte paths list cannot be empty"}

    try:
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            return {"error": "Failed to get Media Storage"}

        clips = media_storage.AddTimelineMattesToMediaPool(matte_paths)
        if clips:
            return {
                "success": True,
                "mattes_added": len(clips),
                "matte_names": [clip.GetName() for clip in clips if clip],
            }
        else:
            return {"error": "Failed to add timeline mattes"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}
