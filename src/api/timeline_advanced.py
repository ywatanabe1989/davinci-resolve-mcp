"""
Advanced Timeline Operations for DaVinci Resolve MCP Server.

Implements timeline duplication, compound clips, generators.
"""

from typing import List


def duplicate_timeline(resolve, timeline_name: str = None, new_name: str = None) -> str:
    """Duplicate a timeline.

    Args:
        timeline_name: Name of the timeline to duplicate (current if None)
        new_name: Name for the duplicated timeline (optional)
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        if timeline_name:
            timeline_count = current_project.GetTimelineCount()
            target_timeline = None
            for i in range(1, timeline_count + 1):
                tl = current_project.GetTimelineByIndex(i)
                if tl and tl.GetName() == timeline_name:
                    target_timeline = tl
                    break
            if not target_timeline:
                return f"Error: Timeline '{timeline_name}' not found"
            current_project.SetCurrentTimeline(target_timeline)
        else:
            target_timeline = current_project.GetCurrentTimeline()
            if not target_timeline:
                return "Error: No timeline currently active"
            timeline_name = target_timeline.GetName()

        if new_name:
            new_timeline = target_timeline.DuplicateTimeline(new_name)
        else:
            new_timeline = target_timeline.DuplicateTimeline()

        if new_timeline:
            return (
                f"Duplicated timeline '{timeline_name}' as '{new_timeline.GetName()}'"
            )
        return f"Failed to duplicate timeline '{timeline_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def _find_timeline_items(current_timeline, clip_names: List[str]) -> List:
    """Helper to find timeline items by name."""
    timeline_items = []
    video_track_count = current_timeline.GetTrackCount("video")
    audio_track_count = current_timeline.GetTrackCount("audio")

    for track_index in range(1, video_track_count + 1):
        items = current_timeline.GetItemListInTrack("video", track_index)
        if items:
            for item in items:
                if item.GetName() in clip_names:
                    timeline_items.append(item)

    for track_index in range(1, audio_track_count + 1):
        items = current_timeline.GetItemListInTrack("audio", track_index)
        if items:
            for item in items:
                if item.GetName() in clip_names:
                    timeline_items.append(item)

    return timeline_items


def create_compound_clip(
    resolve,
    clip_names: List[str],
    compound_name: str = None,
    start_timecode: str = None,
) -> str:
    """Create a compound clip from timeline items."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not clip_names:
        return "Error: Clip names list cannot be empty"

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
        timeline_items = _find_timeline_items(current_timeline, clip_names)
        if not timeline_items:
            return f"Error: No matching clips found for: {', '.join(clip_names)}"

        clip_info = {}
        if compound_name:
            clip_info["name"] = compound_name
        if start_timecode:
            clip_info["startTimecode"] = start_timecode

        result = current_timeline.CreateCompoundClip(timeline_items, clip_info)
        if result:
            return f"Created compound clip from {len(timeline_items)} item(s)"
        return "Failed to create compound clip"
    except Exception as e:
        return f"Error: {str(e)}"


def create_fusion_clip(resolve, clip_names: List[str]) -> str:
    """Create a Fusion clip from timeline items."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not clip_names:
        return "Error: Clip names list cannot be empty"

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
        timeline_items = []
        video_track_count = current_timeline.GetTrackCount("video")
        for track_index in range(1, video_track_count + 1):
            items = current_timeline.GetItemListInTrack("video", track_index)
            if items:
                for item in items:
                    if item.GetName() in clip_names:
                        timeline_items.append(item)

        if not timeline_items:
            return f"Error: No matching clips found for: {', '.join(clip_names)}"

        result = current_timeline.CreateFusionClip(timeline_items)
        if result:
            return f"Created Fusion clip from {len(timeline_items)} item(s)"
        return "Failed to create Fusion clip"
    except Exception as e:
        return f"Error: {str(e)}"


def insert_generator(resolve, generator_name: str) -> str:
    """Insert a generator into the timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not generator_name:
        return "Error: Generator name cannot be empty"

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
        result = current_timeline.InsertGeneratorIntoTimeline(generator_name)
        if result:
            return f"Inserted generator '{generator_name}'"
        return f"Failed to insert generator '{generator_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def insert_fusion_generator(resolve, generator_name: str) -> str:
    """Insert a Fusion generator into the timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not generator_name:
        return "Error: Generator name cannot be empty"

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
        result = current_timeline.InsertFusionGeneratorIntoTimeline(generator_name)
        if result:
            return f"Inserted Fusion generator '{generator_name}'"
        return f"Failed to insert Fusion generator '{generator_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def insert_fusion_composition(resolve) -> str:
    """Insert a Fusion composition into the timeline."""
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
        result = current_timeline.InsertFusionCompositionIntoTimeline()
        if result:
            return "Inserted Fusion composition"
        return "Failed to insert Fusion composition"
    except Exception as e:
        return f"Error: {str(e)}"


def insert_title(resolve, title_name: str) -> str:
    """Insert a title into the timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not title_name:
        return "Error: Title name cannot be empty"

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
        result = current_timeline.InsertTitleIntoTimeline(title_name)
        if result:
            return f"Inserted title '{title_name}'"
        return f"Failed to insert title '{title_name}'"
    except Exception as e:
        return f"Error: {str(e)}"


def insert_fusion_title(resolve, title_name: str) -> str:
    """Insert a Fusion title into the timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not title_name:
        return "Error: Title name cannot be empty"

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
        result = current_timeline.InsertFusionTitleIntoTimeline(title_name)
        if result:
            return f"Inserted Fusion title '{title_name}'"
        return f"Failed to insert Fusion title '{title_name}'"
    except Exception as e:
        return f"Error: {str(e)}"
