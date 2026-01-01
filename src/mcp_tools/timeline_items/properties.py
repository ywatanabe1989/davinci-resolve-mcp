#!/usr/bin/env python3
"""
DaVinci Resolve MCP Timeline Item Property Tools
Getting timeline item properties
"""

from typing import List, Dict, Any


def find_timeline_item(
    timeline, timeline_item_id, search_video=True, search_audio=True
):
    """Find a timeline item by ID across video and audio tracks."""
    if search_video:
        video_track_count = timeline.GetTrackCount("video")
        for track_index in range(1, video_track_count + 1):
            items = timeline.GetItemListInTrack("video", track_index)
            if items:
                for item in items:
                    if str(item.GetUniqueId()) == timeline_item_id:
                        return item, "video"

    if search_audio:
        audio_track_count = timeline.GetTrackCount("audio")
        for track_index in range(1, audio_track_count + 1):
            items = timeline.GetItemListInTrack("audio", track_index)
            if items:
                for item in items:
                    if str(item.GetUniqueId()) == timeline_item_id:
                        return item, "audio"

    return None, None


def register_timeline_item_property_tools(mcp, resolve, logger):
    """Register timeline item property MCP tools and resources."""

    @mcp.resource("resolve://timeline-item/{timeline_item_id}")
    def get_timeline_item_properties(timeline_item_id: str) -> Dict[str, Any]:
        """Get properties of a specific timeline item by ID."""
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
            timeline_item, item_type = find_timeline_item(
                current_timeline, timeline_item_id
            )

            if not timeline_item:
                return {
                    "error": f"Timeline item with ID '{timeline_item_id}' not found"
                }

            properties = {
                "id": timeline_item_id,
                "name": timeline_item.GetName(),
                "type": timeline_item.GetType(),
                "start_frame": timeline_item.GetStart(),
                "end_frame": timeline_item.GetEnd(),
                "duration": timeline_item.GetDuration(),
            }

            if timeline_item.GetType() == "Video":
                properties["transform"] = {
                    "position": {
                        "x": timeline_item.GetProperty("Pan"),
                        "y": timeline_item.GetProperty("Tilt"),
                    },
                    "zoom": timeline_item.GetProperty("ZoomX"),
                    "zoom_x": timeline_item.GetProperty("ZoomX"),
                    "zoom_y": timeline_item.GetProperty("ZoomY"),
                    "rotation": timeline_item.GetProperty("Rotation"),
                    "anchor_point": {
                        "x": timeline_item.GetProperty("AnchorPointX"),
                        "y": timeline_item.GetProperty("AnchorPointY"),
                    },
                    "pitch": timeline_item.GetProperty("Pitch"),
                    "yaw": timeline_item.GetProperty("Yaw"),
                }
                properties["crop"] = {
                    "left": timeline_item.GetProperty("CropLeft"),
                    "right": timeline_item.GetProperty("CropRight"),
                    "top": timeline_item.GetProperty("CropTop"),
                    "bottom": timeline_item.GetProperty("CropBottom"),
                }
                properties["composite"] = {
                    "mode": timeline_item.GetProperty("CompositeMode"),
                    "opacity": timeline_item.GetProperty("Opacity"),
                }
                properties["dynamic_zoom"] = {
                    "enabled": timeline_item.GetProperty("DynamicZoomEnable"),
                    "mode": timeline_item.GetProperty("DynamicZoomMode"),
                }
                properties["retime"] = {
                    "speed": timeline_item.GetProperty("Speed"),
                    "process": timeline_item.GetProperty("RetimeProcess"),
                }
                properties["stabilization"] = {
                    "enabled": timeline_item.GetProperty("StabilizationEnable"),
                    "method": timeline_item.GetProperty("StabilizationMethod"),
                    "strength": timeline_item.GetProperty("StabilizationStrength"),
                }

            if (
                timeline_item.GetType() == "Audio"
                or timeline_item.GetMediaType() == "Audio"
            ):
                properties["audio"] = {
                    "volume": timeline_item.GetProperty("Volume"),
                    "pan": timeline_item.GetProperty("Pan"),
                    "eq_enabled": timeline_item.GetProperty("EQEnable"),
                    "normalize_enabled": timeline_item.GetProperty("NormalizeEnable"),
                    "normalize_level": timeline_item.GetProperty("NormalizeLevel"),
                }

            return properties

        except Exception as e:
            return {"error": f"Error getting timeline item properties: {str(e)}"}

    @mcp.resource("resolve://timeline-items")
    def get_timeline_items() -> List[Dict[str, Any]]:
        """Get all items in the current timeline with their IDs and basic properties."""
        if resolve is None:
            return [{"error": "Not connected to DaVinci Resolve"}]

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return [{"error": "Failed to get Project Manager"}]

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return [{"error": "No project currently open"}]

        current_timeline = current_project.GetCurrentTimeline()
        if not current_timeline:
            return [{"error": "No timeline currently active"}]

        try:
            video_track_count = current_timeline.GetTrackCount("video")
            audio_track_count = current_timeline.GetTrackCount("audio")

            items = []

            for track_index in range(1, video_track_count + 1):
                track_items = current_timeline.GetItemListInTrack("video", track_index)
                if track_items:
                    for item in track_items:
                        items.append(
                            {
                                "id": str(item.GetUniqueId()),
                                "name": item.GetName(),
                                "type": "video",
                                "track": track_index,
                                "start_frame": item.GetStart(),
                                "end_frame": item.GetEnd(),
                                "duration": item.GetDuration(),
                            }
                        )

            for track_index in range(1, audio_track_count + 1):
                track_items = current_timeline.GetItemListInTrack("audio", track_index)
                if track_items:
                    for item in track_items:
                        items.append(
                            {
                                "id": str(item.GetUniqueId()),
                                "name": item.GetName(),
                                "type": "audio",
                                "track": track_index,
                                "start_frame": item.GetStart(),
                                "end_frame": item.GetEnd(),
                                "duration": item.GetDuration(),
                            }
                        )

            if not items:
                return [{"info": "No items found in the current timeline"}]

            return items
        except Exception as e:
            return [{"error": f"Error listing timeline items: {str(e)}"}]

    logger.info("Registered timeline item property tools")
