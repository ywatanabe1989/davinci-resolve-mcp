#!/usr/bin/env python3
"""
DaVinci Resolve Timeline Basic Operations
Timeline creation, listing, and management
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger("davinci-resolve-mcp.timeline.basic")


def list_timelines(resolve) -> List[str]:
    """List all timelines in the current project."""
    if resolve is None:
        return ["Error: Not connected to DaVinci Resolve"]

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return ["Error: Failed to get Project Manager"]

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return ["Error: No project currently open"]

    timeline_count = current_project.GetTimelineCount()
    timelines = []

    for i in range(1, timeline_count + 1):
        timeline = current_project.GetTimelineByIndex(i)
        if timeline:
            timelines.append(timeline.GetName())

    return timelines if timelines else ["No timelines found in the current project"]


def get_current_timeline_info(resolve) -> Dict[str, Any]:
    """Get information about the current timeline."""
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

    info = {
        "name": current_timeline.GetName(),
        "framerate": current_timeline.GetSetting("timelineFrameRate"),
        "resolution": {
            "width": current_timeline.GetSetting("timelineResolutionWidth"),
            "height": current_timeline.GetSetting("timelineResolutionHeight"),
        },
        "start_timecode": current_timeline.GetStartTimecode(),
    }

    return info


def create_timeline(resolve, name: str) -> str:
    """Create a new timeline with the given name."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not name:
        return "Error: Timeline name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return "Error: Failed to get Media Pool"

    existing_timelines = list_timelines(resolve)
    if name in existing_timelines:
        return f"Error: Timeline '{name}' already exists"

    timeline = media_pool.CreateEmptyTimeline(name)
    if timeline:
        return f"Successfully created timeline '{name}'"
    else:
        return f"Failed to create timeline '{name}'"


def create_empty_timeline(
    resolve,
    name: str,
    frame_rate: str = None,
    resolution_width: int = None,
    resolution_height: int = None,
    start_timecode: str = None,
    video_tracks: int = None,
    audio_tracks: int = None,
) -> str:
    """Create a new timeline with the given name and custom settings."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not name:
        return "Error: Timeline name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    media_pool = current_project.GetMediaPool()
    if not media_pool:
        return "Error: Failed to get Media Pool"

    existing_timelines = list_timelines(resolve)
    if name in existing_timelines:
        return f"Error: Timeline '{name}' already exists"

    original_settings = {}
    settings_to_modify = {}

    if frame_rate is not None:
        setting_name = "timelineFrameRate"
        original_settings[setting_name] = current_project.GetSetting(setting_name)
        settings_to_modify[setting_name] = frame_rate

    if resolution_width is not None:
        setting_name = "timelineResolutionWidth"
        original_settings[setting_name] = current_project.GetSetting(setting_name)
        settings_to_modify[setting_name] = str(resolution_width)

    if resolution_height is not None:
        setting_name = "timelineResolutionHeight"
        original_settings[setting_name] = current_project.GetSetting(setting_name)
        settings_to_modify[setting_name] = str(resolution_height)

    for setting_name, setting_value in settings_to_modify.items():
        logger.info(f"Setting project setting {setting_name} to {setting_value}")
        current_project.SetSetting(setting_name, setting_value)

    timeline = media_pool.CreateEmptyTimeline(name)

    if not timeline:
        for setting_name, setting_value in original_settings.items():
            current_project.SetSetting(setting_name, setting_value)
        return f"Failed to create timeline '{name}'"

    current_project.SetCurrentTimeline(timeline)

    if start_timecode is not None:
        try:
            success = timeline.SetStartTimecode(start_timecode)
            if not success:
                logger.warning(f"Failed to set start timecode to {start_timecode}")
        except Exception as e:
            logger.error(f"Error setting start timecode: {str(e)}")

    if video_tracks is not None and video_tracks > 1:
        logger.info(
            f"Custom video track count ({video_tracks}) will need to be set manually"
        )

    if audio_tracks is not None and audio_tracks > 1:
        logger.info(
            f"Custom audio track count ({audio_tracks}) will need to be set manually"
        )

    if original_settings:
        for setting_name, setting_value in original_settings.items():
            current_project.SetSetting(setting_name, setting_value)

    return f"Successfully created timeline '{name}' with custom settings"


def set_current_timeline(resolve, name: str) -> str:
    """Switch to a timeline by name."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not name:
        return "Error: Timeline name cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    timeline_count = current_project.GetTimelineCount()

    for i in range(1, timeline_count + 1):
        timeline = current_project.GetTimelineByIndex(i)
        if timeline and timeline.GetName() == name:
            current_project.SetCurrentTimeline(timeline)
            current_timeline = current_project.GetCurrentTimeline()
            if current_timeline and current_timeline.GetName() == name:
                return f"Successfully switched to timeline '{name}'"
            else:
                return f"Error: Failed to switch to timeline '{name}'"

    return f"Error: Timeline '{name}' not found"


def delete_timeline(resolve, name: str) -> str:
    """Delete a timeline by name."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    timeline_count = current_project.GetTimelineCount()
    target_timeline = None

    for i in range(1, timeline_count + 1):
        timeline = current_project.GetTimelineByIndex(i)
        if timeline and timeline.GetName() == name:
            target_timeline = timeline
            break

    if not target_timeline:
        return f"Error: Timeline '{name}' not found"

    current_timeline = current_project.GetCurrentTimeline()
    if current_timeline and current_timeline.GetName() == name:
        another_timeline = None
        for i in range(1, timeline_count + 1):
            timeline = current_project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() != name:
                another_timeline = timeline
                break

        if another_timeline:
            current_project.SetCurrentTimeline(another_timeline)
        else:
            return f"Error: Cannot delete the only timeline in the project. Create a new timeline first."

    try:
        result = current_project.DeleteTimelines([target_timeline])

        if result:
            return f"Successfully deleted timeline '{name}'"
        else:
            return f"Failed to delete timeline '{name}'"
    except Exception as e:
        return f"Error deleting timeline: {str(e)}"


def get_timeline_tracks(resolve, timeline_name: str = None) -> Dict[str, Any]:
    """Get the track structure of a timeline."""
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    timeline = None
    if timeline_name:
        timeline_count = current_project.GetTimelineCount()
        for i in range(1, timeline_count + 1):
            t = current_project.GetTimelineByIndex(i)
            if t and t.GetName() == timeline_name:
                timeline = t
                break

        if not timeline:
            return {"error": f"Timeline '{timeline_name}' not found"}
    else:
        timeline = current_project.GetCurrentTimeline()
        if not timeline:
            return {"error": "No timeline currently active"}

    timeline_name = timeline.GetName()

    try:
        video_track_count = timeline.GetTrackCount("video")
        audio_track_count = timeline.GetTrackCount("audio")
        subtitle_track_count = timeline.GetTrackCount("subtitle")

        tracks = {
            "name": timeline_name,
            "video": {"count": video_track_count, "tracks": []},
            "audio": {"count": audio_track_count, "tracks": []},
            "subtitle": {"count": subtitle_track_count, "tracks": []},
        }

        for i in range(1, video_track_count + 1):
            track_info = {
                "index": i,
                "name": f"V{i}",
                "enabled": timeline.GetIsTrackEnabled("video", i),
                "clip_count": 0,
            }
            clips = timeline.GetItemListInTrack("video", i)
            track_info["clip_count"] = len(clips) if clips else 0
            tracks["video"]["tracks"].append(track_info)

        for i in range(1, audio_track_count + 1):
            track_info = {
                "index": i,
                "name": f"A{i}",
                "enabled": timeline.GetIsTrackEnabled("audio", i),
                "clip_count": 0,
            }
            clips = timeline.GetItemListInTrack("audio", i)
            track_info["clip_count"] = len(clips) if clips else 0
            tracks["audio"]["tracks"].append(track_info)

        for i in range(1, subtitle_track_count + 1):
            track_info = {
                "index": i,
                "name": f"S{i}",
                "enabled": timeline.GetIsTrackEnabled("subtitle", i),
                "clip_count": 0,
            }
            clips = timeline.GetItemListInTrack("subtitle", i)
            track_info["clip_count"] = len(clips) if clips else 0
            tracks["subtitle"]["tracks"].append(track_info)

        return tracks

    except Exception as e:
        return {"error": f"Error getting timeline tracks: {str(e)}"}
