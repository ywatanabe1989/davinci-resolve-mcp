#!/usr/bin/env python3
"""
DaVinci Resolve Color Grade Operations
LUT application and grade copying
"""

import logging
import os

logger = logging.getLogger("davinci-resolve-mcp.color.grades")


def apply_lut(resolve, lut_path: str, node_index: int = None) -> str:
    """Apply a LUT to a node in the color page."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    if not lut_path:
        return "Error: LUT path cannot be empty"

    if not os.path.exists(lut_path):
        return f"Error: LUT file '{lut_path}' does not exist"

    valid_extensions = [".cube", ".3dl", ".lut", ".mga"]
    file_extension = os.path.splitext(lut_path)[1].lower()
    if file_extension not in valid_extensions:
        return f"Error: Unsupported LUT file format. Supported formats: {', '.join(valid_extensions)}"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"

    try:
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return "Error: No clip is currently selected in the timeline"

        current_grade = current_clip.GetCurrentGrade()
        if not current_grade:
            return "Error: Failed to get current grade"

        target_node_index = node_index
        if target_node_index is None:
            target_node_index = current_grade.GetCurrentNode()
            if target_node_index < 1:
                return "Error: No node is currently selected"
        else:
            node_count = current_grade.GetNodeCount()
            if target_node_index < 1 or target_node_index > node_count:
                return f"Error: Invalid node index {target_node_index}. Valid range: 1-{node_count}"

        result = current_grade.ApplyLUT(target_node_index, lut_path)

        if result:
            try:
                node_name = current_grade.GetNodeName(target_node_index)
                return f"Successfully applied LUT '{os.path.basename(lut_path)}' to node '{node_name}' (index {target_node_index})"
            except Exception:
                return f"Successfully applied LUT '{os.path.basename(lut_path)}' to node {target_node_index}"
        else:
            return f"Failed to apply LUT to node {target_node_index}"

    except Exception as e:
        return f"Error applying LUT: {str(e)}"


def copy_grade(
    resolve,
    source_clip_name: str = None,
    target_clip_name: str = None,
    mode: str = "full",
) -> str:
    """Copy a grade from one clip to another in the color page."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    valid_modes = ["full", "current_node", "all_nodes"]
    if mode.lower() not in valid_modes:
        return f"Error: Invalid copy mode. Must be one of: {', '.join(valid_modes)}"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"

    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"

    try:
        all_video_clips = []
        video_track_count = current_timeline.GetTrackCount("video")

        for track_index in range(1, video_track_count + 1):
            track_items = current_timeline.GetItemListInTrack("video", track_index)
            if track_items:
                all_video_clips.extend(track_items)

        source_clip = None
        if source_clip_name:
            for clip in all_video_clips:
                if clip and clip.GetName() == source_clip_name:
                    source_clip = clip
                    break

            if not source_clip:
                return f"Error: Source clip '{source_clip_name}' not found in timeline"
        else:
            source_clip = current_timeline.GetCurrentVideoItem()
            if not source_clip:
                return "Error: No clip is currently selected to use as source"
            source_clip_name = source_clip.GetName()

        source_grade = source_clip.GetCurrentGrade()
        if not source_grade:
            return f"Error: Failed to get grade from source clip '{source_clip_name}'"

        target_clip = None
        if target_clip_name:
            if target_clip_name == source_clip_name:
                return f"Error: Source and target clips cannot be the same (both are '{source_clip_name}')"

            for clip in all_video_clips:
                if clip and clip.GetName() == target_clip_name:
                    target_clip = clip
                    break

            if not target_clip:
                return f"Error: Target clip '{target_clip_name}' not found in timeline"
        else:
            current_clip = current_timeline.GetCurrentVideoItem()

            if not current_clip:
                return "Error: No clip is currently selected to use as target"

            if current_clip.GetName() == source_clip_name:
                return "Error: Cannot copy grade to the same clip. Please specify a different target clip."

            target_clip = current_clip
            target_clip_name = target_clip.GetName()

        target_grade = target_clip.GetCurrentGrade()
        if not target_grade:
            return f"Error: Failed to get grade from target clip '{target_clip_name}'"

        current_timeline.SetCurrentVideoItem(target_clip)

        result = False
        if mode.lower() == "full":
            result = target_clip.CopyGrade(source_clip)
        elif mode.lower() == "current_node":
            source_node_index = source_grade.GetCurrentNode()
            target_node_index = target_grade.GetCurrentNode()

            if source_node_index < 1:
                return "Error: No node selected in source clip"

            if target_node_index < 1:
                return "Error: No node selected in target clip"

            result = target_grade.CopyFromNodeToNode(
                source_grade, source_node_index, target_node_index
            )
        elif mode.lower() == "all_nodes":
            source_node_count = source_grade.GetNodeCount()

            if source_node_count < 1:
                return "Error: Source clip has no nodes to copy"

            target_node_count = target_grade.GetNodeCount()
            for i in range(target_node_count, 0, -1):
                target_grade.DeleteNode(i)

            for i in range(1, source_node_count + 1):
                if source_grade.IsSerial(i):
                    target_grade.AddSerialNode()
                elif source_grade.IsParallel(i):
                    target_grade.AddParallelNode()
                elif source_grade.IsLayer(i):
                    target_grade.AddLayerNode()

                new_node_index = target_grade.GetCurrentNode()
                if new_node_index > 0:
                    target_grade.CopyFromNodeToNode(source_grade, i, new_node_index)

            result = True

        if result:
            return f"Successfully copied grade from '{source_clip_name}' to '{target_clip_name}' using mode '{mode}'"
        else:
            return f"Failed to copy grade from '{source_clip_name}' to '{target_clip_name}' using mode '{mode}'"

    except Exception as e:
        return f"Error copying grade: {str(e)}"
