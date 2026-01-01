#!/usr/bin/env python3
"""
DaVinci Resolve Timeline Marker Operations
Adding and managing timeline markers
"""

import logging
from typing import Optional

logger = logging.getLogger("davinci-resolve-mcp.timeline.markers")


def add_marker(
    resolve, frame: Optional[int] = None, color: str = "Blue", note: str = ""
) -> str:
    """Add a marker at the specified frame in the current timeline."""
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
        timeline_start = current_timeline.GetStartFrame()
        timeline_end = current_timeline.GetEndFrame()
        timeline_name = current_timeline.GetName()
        print(
            f"Timeline '{timeline_name}' frame range: {timeline_start}-{timeline_end}"
        )
    except Exception as e:
        return f"Error: Failed to get timeline information: {str(e)}"

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
        return (
            f"Error: Invalid marker color. Valid colors are: {', '.join(valid_colors)}"
        )

    try:
        clips = []
        for track_idx in range(1, 5):
            try:
                track_clips = current_timeline.GetItemListInTrack("video", track_idx)
                if track_clips and len(track_clips) > 0:
                    clips.extend(track_clips)
            except Exception:
                continue

        if not clips:
            return "Error: No clips found in timeline. Add media to the timeline first."

        existing_markers = current_timeline.GetMarkers() or {}

        if frame is None:
            for clip in clips:
                clip_start = clip.GetStart()
                clip_end = clip.GetEnd()

                mid_frame = clip_start + ((clip_end - clip_start) // 2)
                if mid_frame not in existing_markers:
                    frame = mid_frame
                    break

                if (mid_frame + 1) not in existing_markers:
                    frame = mid_frame + 1
                    break

                for offset in [10, 20, 30, 40, 50]:
                    test_frame = clip_start + offset
                    if (
                        clip_start <= test_frame <= clip_end
                        and test_frame not in existing_markers
                    ):
                        frame = test_frame
                        break

            if frame is None:
                for f in range(timeline_start, timeline_end, 10):
                    if f not in existing_markers:
                        for clip in clips:
                            if clip.GetStart() <= f <= clip.GetEnd():
                                frame = f
                                break
                    if frame is not None:
                        break

            if frame is None:
                return "Error: Could not find a valid frame position for marker. Try specifying a frame number."

        else:
            if frame < timeline_start or frame > timeline_end:
                return f"Error: Frame {frame} is out of timeline bounds ({timeline_start}-{timeline_end})"

            if frame in existing_markers:
                alternates = [frame + 1, frame - 1, frame + 2, frame + 5, frame + 10]

                for alt_frame in alternates:
                    if (
                        timeline_start <= alt_frame <= timeline_end
                        and alt_frame not in existing_markers
                    ):
                        for clip in clips:
                            if clip.GetStart() <= alt_frame <= clip.GetEnd():
                                return f"Error: A marker already exists at frame {frame}. Try frame {alt_frame} instead."

                return f"Error: A marker already exists at frame {frame}. Try a different frame position."

            frame_in_clip = False
            for clip in clips:
                if clip.GetStart() <= frame <= clip.GetEnd():
                    frame_in_clip = True
                    break

            if not frame_in_clip:
                return f"Error: Frame {frame} is not within any media in the timeline. Markers must be on actual clips."

        print(f"Adding marker at frame {frame} with color {color}")
        marker_result = current_timeline.AddMarker(
            frame,
            color,
            note,
            note,
            1,
            "",
        )

        if marker_result:
            return (
                f"Successfully added {color} marker at frame {frame} with note: {note}"
            )
        else:
            return f"Failed to add marker at frame {frame}"

    except Exception as e:
        return f"Error adding marker: {str(e)}"
