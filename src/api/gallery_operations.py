"""
Gallery Operations for DaVinci Resolve MCP Server.

Implements Gallery APIs for stills and power grades management.
"""

from typing import List, Dict, Any


def get_gallery_still_albums(resolve) -> List[Dict[str, str]]:
    """Get list of gallery still albums."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return [{"error": "No project currently open"}]

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return [{"error": "Failed to get Gallery"}]

        albums = gallery.GetGalleryStillAlbums()
        if not albums:
            return []

        result = []
        for album in albums:
            result.append(
                {
                    "name": gallery.GetAlbumName(album),
                    "still_count": len(album.GetStills()) if album.GetStills() else 0,
                }
            )
        return result
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]


def get_gallery_power_grade_albums(resolve) -> List[Dict[str, str]]:
    """Get list of gallery PowerGrade albums."""
    if resolve is None:
        return [{"error": "Not connected to DaVinci Resolve"}]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return [{"error": "Failed to get Project Manager"}]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return [{"error": "No project currently open"}]

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return [{"error": "Failed to get Gallery"}]

        albums = gallery.GetGalleryPowerGradeAlbums()
        if not albums:
            return []

        result = []
        for album in albums:
            result.append(
                {
                    "name": gallery.GetAlbumName(album),
                    "still_count": len(album.GetStills()) if album.GetStills() else 0,
                }
            )
        return result
    except Exception as e:
        return [{"error": f"Error: {str(e)}"}]


def get_current_still_album(resolve) -> Dict[str, Any]:
    """Get the current still album."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return {"error": "Failed to get Gallery"}

        album = gallery.GetCurrentStillAlbum()
        if not album:
            return {"error": "No current still album"}

        stills = album.GetStills()
        return {
            "name": gallery.GetAlbumName(album),
            "still_count": len(stills) if stills else 0,
        }
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def create_still_album(resolve) -> str:
    """Create a new gallery still album."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        album = gallery.CreateGalleryStillAlbum()
        if album:
            return f"Successfully created still album: {gallery.GetAlbumName(album)}"
        else:
            return "Failed to create still album"
    except Exception as e:
        return f"Error: {str(e)}"


def create_power_grade_album(resolve) -> str:
    """Create a new gallery PowerGrade album."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        album = gallery.CreateGalleryPowerGradeAlbum()
        if album:
            return (
                f"Successfully created PowerGrade album: {gallery.GetAlbumName(album)}"
            )
        else:
            return "Failed to create PowerGrade album"
    except Exception as e:
        return f"Error: {str(e)}"


def set_album_name(resolve, old_name: str, new_name: str) -> str:
    """Rename a gallery album.

    Args:
        old_name: Current name of the album
        new_name: New name for the album
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not old_name or not new_name:
        return "Error: Album names cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        # Search in still albums
        albums = gallery.GetGalleryStillAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == old_name:
                result = gallery.SetAlbumName(album, new_name)
                if result:
                    return f"Successfully renamed album '{old_name}' to '{new_name}'"
                else:
                    return f"Failed to rename album '{old_name}'"

        # Search in PowerGrade albums
        albums = gallery.GetGalleryPowerGradeAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == old_name:
                result = gallery.SetAlbumName(album, new_name)
                if result:
                    return f"Successfully renamed album '{old_name}' to '{new_name}'"
                else:
                    return f"Failed to rename album '{old_name}'"

        return f"Error: Album '{old_name}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


def set_current_still_album(resolve, album_name: str) -> str:
    """Set the current still album by name.

    Args:
        album_name: Name of the album to set as current
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not album_name:
        return "Error: Album name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        albums = gallery.GetGalleryStillAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == album_name:
                result = gallery.SetCurrentStillAlbum(album)
                if result:
                    return f"Successfully set current album to '{album_name}'"
                else:
                    return f"Failed to set current album to '{album_name}'"

        return f"Error: Album '{album_name}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


def grab_still(resolve) -> str:
    """Grab a still from the current video clip."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"

    try:
        still = current_timeline.GrabStill()
        if still:
            return "Successfully grabbed still from current clip"
        else:
            return "Failed to grab still (ensure you're on the Color page)"
    except Exception as e:
        return f"Error: {str(e)}"


def grab_all_stills(resolve, source: int = 1) -> Dict[str, Any]:
    """Grab stills from all clips in the timeline.

    Args:
        source: 1 for first frame, 2 for middle frame
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    if source not in [1, 2]:
        return {"error": "Source must be 1 (first frame) or 2 (middle frame)"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}

    try:
        stills = current_timeline.GrabAllStills(source)
        if stills:
            return {
                "success": True,
                "stills_grabbed": len(stills),
                "source": "first frame" if source == 1 else "middle frame",
            }
        else:
            return {"error": "Failed to grab stills (ensure you're on the Color page)"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def import_stills(resolve, album_name: str, file_paths: List[str]) -> str:
    """Import still images into a gallery album.

    Args:
        album_name: Name of the album to import stills into
        file_paths: List of file paths to import
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not album_name or not file_paths:
        return "Error: Album name and file paths are required"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        # Find the album
        target_album = None
        albums = gallery.GetGalleryStillAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == album_name:
                target_album = album
                break

        if not target_album:
            return f"Error: Album '{album_name}' not found"

        result = target_album.ImportStills(file_paths)
        if result:
            return f"Successfully imported {len(file_paths)} still(s) into album '{album_name}'"
        else:
            return f"Failed to import stills into album '{album_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def export_stills(
    resolve,
    album_name: str,
    folder_path: str,
    file_prefix: str = "still",
    format: str = "dpx",
) -> str:
    """Export stills from a gallery album.

    Args:
        album_name: Name of the album to export from
        folder_path: Directory to export to
        file_prefix: Filename prefix (default: 'still')
        format: Export format (dpx, cin, tif, jpg, png, ppm, bmp, xpm, drx)
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not album_name or not folder_path:
        return "Error: Album name and folder path are required"

    valid_formats = ["dpx", "cin", "tif", "jpg", "png", "ppm", "bmp", "xpm", "drx"]
    if format not in valid_formats:
        return f"Error: Invalid format. Must be one of: {', '.join(valid_formats)}"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        # Find the album
        target_album = None
        albums = gallery.GetGalleryStillAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == album_name:
                target_album = album
                break

        if not target_album:
            return f"Error: Album '{album_name}' not found"

        stills = target_album.GetStills()
        if not stills:
            return f"Error: No stills in album '{album_name}'"

        result = target_album.ExportStills(stills, folder_path, file_prefix, format)
        if result:
            return f"Successfully exported {len(stills)} still(s) from album '{album_name}'"
        else:
            return f"Failed to export stills from album '{album_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_stills(resolve, album_name: str) -> str:
    """Delete all stills from a gallery album.

    Args:
        album_name: Name of the album to delete stills from
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not album_name:
        return "Error: Album name is required"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        gallery = current_project.GetGallery()
        if not gallery:
            return "Error: Failed to get Gallery"

        # Find the album
        target_album = None
        albums = gallery.GetGalleryStillAlbums()
        for album in albums or []:
            if gallery.GetAlbumName(album) == album_name:
                target_album = album
                break

        if not target_album:
            return f"Error: Album '{album_name}' not found"

        stills = target_album.GetStills()
        if not stills:
            return f"No stills to delete in album '{album_name}'"

        result = target_album.DeleteStills(stills)
        if result:
            return (
                f"Successfully deleted {len(stills)} still(s) from album '{album_name}'"
            )
        else:
            return f"Failed to delete stills from album '{album_name}'"
    except Exception as e:
        return f"Error: {str(e)}"
