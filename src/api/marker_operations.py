"""
Marker Operations for DaVinci Resolve MCP Server.

Implements comprehensive marker management for timelines and clips.
"""

from typing import Dict, Any


def get_timeline_markers(resolve) -> Dict[str, Any]:
    """Get all markers from the current timeline."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

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
        markers = current_timeline.GetMarkers()
        if markers:
            return {"markers": markers, "count": len(markers)}
        return {"markers": {}, "count": 0}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def add_timeline_marker(
    resolve,
    frame: int,
    color: str = "Blue",
    name: str = "",
    note: str = "",
    duration: int = 1,
    custom_data: str = "",
) -> str:
    """Add a marker to the current timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    valid_colors = [
        "Blue",
        "Cyan",
        "Green",
        "Yellow",
        "Red",
        "Pink",
        "Purple",
        "Fuchsia",
        "Rose",
        "Lavender",
        "Sky",
        "Mint",
        "Lemon",
        "Sand",
        "Cocoa",
        "Cream",
    ]
    if color not in valid_colors:
        return f"Error: Invalid color. Use: {', '.join(valid_colors)}"

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
        result = current_timeline.AddMarker(
            frame, color, name, note, duration, custom_data
        )
        if result:
            return f"Added {color} marker at frame {frame}"
        return f"Failed to add marker at frame {frame}"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_timeline_marker_at_frame(resolve, frame: int) -> str:
    """Delete a marker at the specified frame."""
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
        result = current_timeline.DeleteMarkerAtFrame(frame)
        if result:
            return f"Deleted marker at frame {frame}"
        return f"No marker found at frame {frame}"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_timeline_markers_by_color(resolve, color: str) -> str:
    """Delete all markers of the specified color."""
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
        result = current_timeline.DeleteMarkersByColor(color)
        if result:
            return f"Deleted all {color} markers"
        return f"No {color} markers found"
    except Exception as e:
        return f"Error: {str(e)}"


def get_marker_by_custom_data(resolve, custom_data: str) -> Dict[str, Any]:
    """Find a marker by its custom data."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    if not custom_data:
        return {"error": "Custom data cannot be empty"}

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
        marker = current_timeline.GetMarkerByCustomData(custom_data)
        if marker:
            return {"marker": marker}
        return {"error": "No marker found with specified custom data"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def update_marker_custom_data(resolve, frame: int, custom_data: str) -> str:
    """Update the custom data of a marker at the specified frame."""
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
        result = current_timeline.UpdateMarkerCustomData(frame, custom_data)
        if result:
            return f"Updated custom data for marker at frame {frame}"
        return f"Failed to update marker at frame {frame}"
    except Exception as e:
        return f"Error: {str(e)}"


def get_marker_custom_data(resolve, frame: int) -> str:
    """Get the custom data of a marker at the specified frame."""
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
        data = current_timeline.GetMarkerCustomData(frame)
        return data if data else "No custom data found"
    except Exception as e:
        return f"Error: {str(e)}"


def delete_marker_by_custom_data(resolve, custom_data: str) -> str:
    """Delete the first marker with the specified custom data."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not custom_data:
        return "Error: Custom data cannot be empty"

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
        result = current_timeline.DeleteMarkerByCustomData(custom_data)
        if result:
            return "Deleted marker with specified custom data"
        return "No marker found with specified custom data"
    except Exception as e:
        return f"Error: {str(e)}"


def get_clip_markers(resolve, clip_name: str) -> Dict[str, Any]:
    """Get all markers from a media pool clip."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    if not clip_name:
        return {"error": "Clip name cannot be empty"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return {"error": "Failed to get Media Pool"}

    try:
        # Find the clip
        def find_clip(folder):
            clips = folder.GetClipList()
            if clips:
                for clip in clips:
                    if clip.GetName() == clip_name:
                        return clip
            for subfolder in folder.GetSubFolderList():
                result = find_clip(subfolder)
                if result:
                    return result
            return None

        clip = find_clip(media_pool.GetRootFolder())
        if not clip:
            return {"error": f"Clip '{clip_name}' not found"}

        markers = clip.GetMarkers()
        if markers:
            return {"clip": clip_name, "markers": markers, "count": len(markers)}
        return {"clip": clip_name, "markers": {}, "count": 0}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def add_clip_marker(
    resolve,
    clip_name: str,
    frame: int,
    color: str = "Blue",
    name: str = "",
    note: str = "",
    duration: int = 1,
    custom_data: str = "",
) -> str:
    """Add a marker to a media pool clip."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not clip_name:
        return "Error: Clip name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return "Error: Failed to get Media Pool"

    try:

        def find_clip(folder):
            clips = folder.GetClipList()
            if clips:
                for clip in clips:
                    if clip.GetName() == clip_name:
                        return clip
            for subfolder in folder.GetSubFolderList():
                result = find_clip(subfolder)
                if result:
                    return result
            return None

        clip = find_clip(media_pool.GetRootFolder())
        if not clip:
            return f"Error: Clip '{clip_name}' not found"

        result = clip.AddMarker(frame, color, name, note, duration, custom_data)
        if result:
            return f"Added {color} marker at frame {frame} on clip '{clip_name}'"
        return f"Failed to add marker on clip '{clip_name}'"
    except Exception as e:
        return f"Error: {str(e)}"
