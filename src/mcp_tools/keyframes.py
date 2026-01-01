#!/usr/bin/env python3
"""
DaVinci Resolve MCP Keyframe Tools
Keyframe control and animation
"""

from typing import Dict, Any


def register_keyframe_tools(mcp, resolve, logger):
    """Register keyframe MCP tools and resources."""

    def find_timeline_item(timeline, timeline_item_id):
        """Find a timeline item by ID across video and audio tracks."""
        video_track_count = timeline.GetTrackCount("video")
        for track_index in range(1, video_track_count + 1):
            items = timeline.GetItemListInTrack("video", track_index)
            if items:
                for item in items:
                    if str(item.GetUniqueId()) == timeline_item_id:
                        return item, "video"

        audio_track_count = timeline.GetTrackCount("audio")
        for track_index in range(1, audio_track_count + 1):
            items = timeline.GetItemListInTrack("audio", track_index)
            if items:
                for item in items:
                    if str(item.GetUniqueId()) == timeline_item_id:
                        return item, "audio"

        return None, None

    @mcp.resource(
        "resolve://timeline-item/{timeline_item_id}/keyframes/{property_name}"
    )
    def get_timeline_item_keyframes(
        timeline_item_id: str, property_name: str
    ) -> Dict[str, Any]:
        """Get keyframes for a specific timeline item by ID."""
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
            timeline_item, _ = find_timeline_item(current_timeline, timeline_item_id)

            if not timeline_item:
                return {
                    "error": f"Timeline item with ID '{timeline_item_id}' not found"
                }

            video_properties = [
                "Pan",
                "Tilt",
                "ZoomX",
                "ZoomY",
                "Rotation",
                "AnchorPointX",
                "AnchorPointY",
                "Pitch",
                "Yaw",
                "Opacity",
                "CropLeft",
                "CropRight",
                "CropTop",
                "CropBottom",
            ]
            audio_properties = ["Volume", "Pan"]

            keyframeable_properties = []
            keyframes = {}

            if timeline_item.GetType() == "Video":
                for prop in video_properties:
                    if timeline_item.GetKeyframeCount(prop) > 0:
                        keyframeable_properties.append(prop)
                        keyframes[prop] = []
                        keyframe_count = timeline_item.GetKeyframeCount(prop)
                        for i in range(keyframe_count):
                            frame_pos = timeline_item.GetKeyframeAtIndex(prop, i)[
                                "frame"
                            ]
                            value = timeline_item.GetPropertyAtKeyframeIndex(prop, i)
                            keyframes[prop].append({"frame": frame_pos, "value": value})

            if (
                timeline_item.GetType() == "Audio"
                or timeline_item.GetMediaType() == "Audio"
            ):
                for prop in audio_properties:
                    if timeline_item.GetKeyframeCount(prop) > 0:
                        keyframeable_properties.append(prop)
                        keyframes[prop] = []
                        keyframe_count = timeline_item.GetKeyframeCount(prop)
                        for i in range(keyframe_count):
                            frame_pos = timeline_item.GetKeyframeAtIndex(prop, i)[
                                "frame"
                            ]
                            value = timeline_item.GetPropertyAtKeyframeIndex(prop, i)
                            keyframes[prop].append({"frame": frame_pos, "value": value})

            if property_name:
                if property_name in keyframes:
                    return {
                        "item_id": timeline_item_id,
                        "item_name": timeline_item.GetName(),
                        "properties": [property_name],
                        "keyframes": {property_name: keyframes[property_name]},
                    }
                else:
                    return {
                        "item_id": timeline_item_id,
                        "item_name": timeline_item.GetName(),
                        "properties": [],
                        "keyframes": {},
                    }

            return {
                "item_id": timeline_item_id,
                "item_name": timeline_item.GetName(),
                "properties": keyframeable_properties,
                "keyframes": keyframes,
            }

        except Exception as e:
            return {"error": f"Error getting timeline item keyframes: {str(e)}"}

    @mcp.tool()
    def add_keyframe(
        timeline_item_id: str, property_name: str, frame: int, value: float
    ) -> str:
        """Add a keyframe at the specified frame for a timeline item property."""
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

        video_properties = [
            "Pan",
            "Tilt",
            "ZoomX",
            "ZoomY",
            "Rotation",
            "AnchorPointX",
            "AnchorPointY",
            "Pitch",
            "Yaw",
            "Opacity",
            "CropLeft",
            "CropRight",
            "CropTop",
            "CropBottom",
        ]
        audio_properties = ["Volume", "Pan"]
        valid_properties = video_properties + audio_properties

        if property_name not in valid_properties:
            return f"Error: Invalid property. Must be one of: {', '.join(valid_properties)}"

        try:
            timeline_item, item_type = find_timeline_item(
                current_timeline, timeline_item_id
            )

            if not timeline_item:
                return f"Error: Timeline item with ID '{timeline_item_id}' not found"

            is_audio = item_type == "audio"
            if is_audio and property_name not in audio_properties:
                return f"Error: Property '{property_name}' is not available for audio items"

            start_frame = timeline_item.GetStart()
            end_frame = timeline_item.GetEnd()

            if frame < start_frame or frame > end_frame:
                return f"Error: Frame {frame} is outside the item's range ({start_frame} to {end_frame})"

            result = timeline_item.AddKeyframe(property_name, frame, value)

            if result:
                return f"Successfully added keyframe for {property_name} at frame {frame} with value {value}"
            else:
                return f"Failed to add keyframe for {property_name} at frame {frame}"

        except Exception as e:
            return f"Error adding keyframe: {str(e)}"

    @mcp.tool()
    def modify_keyframe(
        timeline_item_id: str,
        property_name: str,
        frame: int,
        new_value: float = None,
        new_frame: int = None,
    ) -> str:
        """Modify an existing keyframe by changing its value or frame position."""
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

        if new_value is None and new_frame is None:
            return "Error: Must specify at least one of new_value or new_frame"

        try:
            timeline_item, _ = find_timeline_item(current_timeline, timeline_item_id)

            if not timeline_item:
                return f"Error: Timeline item with ID '{timeline_item_id}' not found"

            keyframe_count = timeline_item.GetKeyframeCount(property_name)
            if keyframe_count == 0:
                return f"Error: No keyframes found for property '{property_name}'"

            keyframe_index = -1
            for i in range(keyframe_count):
                kf = timeline_item.GetKeyframeAtIndex(property_name, i)
                if kf["frame"] == frame:
                    keyframe_index = i
                    break

            if keyframe_index == -1:
                return f"Error: No keyframe found at frame {frame} for property '{property_name}'"

            if new_frame is not None:
                start_frame = timeline_item.GetStart()
                end_frame = timeline_item.GetEnd()

                if new_frame < start_frame or new_frame > end_frame:
                    return f"Error: New frame {new_frame} is outside the item's range"

                current_value = timeline_item.GetPropertyAtKeyframeIndex(
                    property_name, keyframe_index
                )
                timeline_item.DeleteKeyframe(property_name, frame)
                value = new_value if new_value is not None else current_value
                result = timeline_item.AddKeyframe(property_name, new_frame, value)

                if result:
                    return f"Successfully moved keyframe from frame {frame} to frame {new_frame}"
                else:
                    return f"Failed to move keyframe for {property_name}"
            else:
                timeline_item.DeleteKeyframe(property_name, frame)
                result = timeline_item.AddKeyframe(property_name, frame, new_value)

                if result:
                    return f"Successfully updated keyframe value to {new_value}"
                else:
                    return f"Failed to update keyframe value"

        except Exception as e:
            return f"Error modifying keyframe: {str(e)}"

    @mcp.tool()
    def delete_keyframe(timeline_item_id: str, property_name: str, frame: int) -> str:
        """Delete a keyframe at the specified frame for a timeline item property."""
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
            timeline_item, _ = find_timeline_item(current_timeline, timeline_item_id)

            if not timeline_item:
                return f"Error: Timeline item with ID '{timeline_item_id}' not found"

            keyframe_count = timeline_item.GetKeyframeCount(property_name)
            if keyframe_count == 0:
                return f"Error: No keyframes found for property '{property_name}'"

            keyframe_exists = False
            for i in range(keyframe_count):
                kf = timeline_item.GetKeyframeAtIndex(property_name, i)
                if kf["frame"] == frame:
                    keyframe_exists = True
                    break

            if not keyframe_exists:
                return f"Error: No keyframe found at frame {frame}"

            result = timeline_item.DeleteKeyframe(property_name, frame)

            if result:
                return f"Successfully deleted keyframe for {property_name} at frame {frame}"
            else:
                return f"Failed to delete keyframe"

        except Exception as e:
            return f"Error deleting keyframe: {str(e)}"

    @mcp.tool()
    def set_keyframe_interpolation(
        timeline_item_id: str, property_name: str, frame: int, interpolation_type: str
    ) -> str:
        """Set the interpolation type for a keyframe."""
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

        valid_interpolation_types = ["Linear", "Bezier", "Ease-In", "Ease-Out"]
        if interpolation_type not in valid_interpolation_types:
            return f"Error: Invalid interpolation. Must be one of: {', '.join(valid_interpolation_types)}"

        try:
            timeline_item, _ = find_timeline_item(current_timeline, timeline_item_id)

            if not timeline_item:
                return f"Error: Timeline item with ID '{timeline_item_id}' not found"

            keyframe_count = timeline_item.GetKeyframeCount(property_name)
            if keyframe_count == 0:
                return f"Error: No keyframes found for property '{property_name}'"

            keyframe_exists = False
            value = None
            for i in range(keyframe_count):
                kf = timeline_item.GetKeyframeAtIndex(property_name, i)
                if kf["frame"] == frame:
                    keyframe_exists = True
                    value = timeline_item.GetPropertyAtKeyframeIndex(property_name, i)
                    break

            if not keyframe_exists:
                return f"Error: No keyframe found at frame {frame}"

            interpolation_map = {"Linear": 0, "Bezier": 1, "Ease-In": 2, "Ease-Out": 3}

            timeline_item.DeleteKeyframe(property_name, frame)
            result = timeline_item.AddKeyframe(
                property_name, frame, value, interpolation_map[interpolation_type]
            )

            if result:
                return f"Successfully set interpolation to {interpolation_type}"
            else:
                return f"Failed to set interpolation"

        except Exception as e:
            return f"Error setting keyframe interpolation: {str(e)}"

    @mcp.tool()
    def enable_keyframes(timeline_item_id: str, keyframe_mode: str = "All") -> str:
        """Enable keyframe mode for a timeline item."""
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

        valid_keyframe_modes = ["All", "Color", "Sizing"]
        if keyframe_mode not in valid_keyframe_modes:
            return f"Error: Invalid mode. Must be one of: {', '.join(valid_keyframe_modes)}"

        try:
            video_track_count = current_timeline.GetTrackCount("video")
            timeline_item = None

            for track_index in range(1, video_track_count + 1):
                items = current_timeline.GetItemListInTrack("video", track_index)
                if items:
                    for item in items:
                        if str(item.GetUniqueId()) == timeline_item_id:
                            timeline_item = item
                            break
                if timeline_item:
                    break

            if not timeline_item:
                return (
                    f"Error: Video timeline item with ID '{timeline_item_id}' not found"
                )

            if timeline_item.GetType() != "Video":
                return f"Error: Timeline item is not a video item"

            keyframe_mode_map = {"All": 0, "Color": 1, "Sizing": 2}
            result = timeline_item.SetProperty(
                "KeyframeMode", keyframe_mode_map[keyframe_mode]
            )

            if result:
                return f"Successfully enabled {keyframe_mode} keyframe mode"
            else:
                return f"Failed to enable {keyframe_mode} keyframe mode"

        except Exception as e:
            return f"Error enabling keyframe mode: {str(e)}"

    logger.info("Registered keyframe tools")
