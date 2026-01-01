#!/usr/bin/env python3
"""
DaVinci Resolve MCP LUT Tools
LUT export and management
"""

import os
from typing import Dict, Any


def register_lut_tools(mcp, resolve, logger):
    """Register LUT MCP tools and resources."""

    @mcp.resource("resolve://color/lut-formats")
    def get_lut_formats() -> Dict[str, Any]:
        """Get available LUT export formats and sizes."""
        return {
            "formats": [
                {
                    "name": "Cube",
                    "extension": ".cube",
                    "description": "Industry standard LUT format",
                },
                {
                    "name": "Davinci",
                    "extension": ".ilut",
                    "description": "DaVinci Resolve native format",
                },
                {
                    "name": "3dl",
                    "extension": ".3dl",
                    "description": "ASSIMILATE SCRATCH format",
                },
                {
                    "name": "Panasonic",
                    "extension": ".vlut",
                    "description": "Panasonic VariCam format",
                },
            ],
            "sizes": [
                {"name": "17Point", "description": "Smaller file size (17x17x17)"},
                {"name": "33Point", "description": "Standard size (33x33x33)"},
                {"name": "65Point", "description": "Highest precision (65x65x65)"},
            ],
        }

    @mcp.tool()
    def export_lut(
        clip_name: str = None,
        export_path: str = None,
        lut_format: str = "Cube",
        lut_size: str = "33Point",
    ) -> str:
        """Export a LUT from the current clip's grade."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_page = resolve.GetCurrentPage()
        if current_page != "color":
            resolve.OpenPage("color")

        try:
            current_timeline = current_project.GetCurrentTimeline()
            if not current_timeline:
                return "Error: No timeline is currently open"

            if clip_name:
                timeline_clips = current_timeline.GetItemListInTrack("video", 1)
                target_clip = None
                for clip in timeline_clips:
                    if clip.GetName() == clip_name:
                        target_clip = clip
                        break
                if not target_clip:
                    return f"Error: Clip '{clip_name}' not found in the timeline"
                current_timeline.SetCurrentSelectedItem(target_clip)

            if not export_path:
                import tempfile

                clip_name_safe = clip_name if clip_name else "current_clip"
                clip_name_safe = clip_name_safe.replace(" ", "_").replace(":", "-")
                extension = ".cube"
                if lut_format.lower() == "davinci":
                    extension = ".ilut"
                elif lut_format.lower() == "3dl":
                    extension = ".3dl"
                elif lut_format.lower() == "panasonic":
                    extension = ".vlut"
                export_path = os.path.join(
                    tempfile.gettempdir(), f"{clip_name_safe}_lut{extension}"
                )

            valid_formats = ["Cube", "Davinci", "3dl", "Panasonic"]
            if lut_format not in valid_formats:
                return f"Error: Invalid LUT format"

            valid_sizes = ["17Point", "33Point", "65Point"]
            if lut_size not in valid_sizes:
                return f"Error: Invalid LUT size"

            format_map = {"Cube": 0, "Davinci": 1, "3dl": 2, "Panasonic": 3}
            size_map = {"17Point": 0, "33Point": 1, "65Point": 2}

            current_clip = current_timeline.GetCurrentVideoItem()
            if not current_clip:
                return "Error: No clip is currently selected"

            export_dir = os.path.dirname(export_path)
            if export_dir and not os.path.exists(export_dir):
                os.makedirs(export_dir, exist_ok=True)

            result = current_project.ExportCurrentGradeAsLUT(
                format_map[lut_format], size_map[lut_size], export_path
            )

            if current_page != "color":
                resolve.OpenPage(current_page)

            if result:
                return f"Successfully exported LUT to '{export_path}'"
            else:
                return "Failed to export LUT"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error exporting LUT: {str(e)}"

    @mcp.tool()
    def export_all_powergrade_luts(export_dir: str) -> str:
        """Export all PowerGrade presets as LUT files."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return "Error: Failed to get Project Manager"

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return "Error: No project currently open"

        current_page = resolve.GetCurrentPage()
        if current_page != "color":
            resolve.OpenPage("color")

        try:
            gallery = current_project.GetGallery()
            if not gallery:
                return "Error: Failed to get gallery"

            powergrade_album = None
            albums = gallery.GetAlbums()

            if albums:
                for album in albums:
                    if album.GetName() == "PowerGrade":
                        powergrade_album = album
                        break

            if not powergrade_album:
                return "Error: PowerGrade album not found"

            stills = powergrade_album.GetStills()
            if not stills:
                return "Error: No stills found in PowerGrade album"

            if not os.path.exists(export_dir):
                os.makedirs(export_dir, exist_ok=True)

            current_timeline = current_project.GetCurrentTimeline()
            exported_count = 0
            failed_stills = []

            for still in stills:
                still_name = still.GetLabel()
                if not still_name:
                    still_name = f"PowerGrade_{still.GetUniqueId()}"

                safe_name = "".join(
                    c if c.isalnum() or c in ["-", "_"] else "_" for c in still_name
                )
                lut_path = os.path.join(export_dir, f"{safe_name}.cube")

                current_clip = current_timeline.GetCurrentVideoItem()
                if not current_clip:
                    failed_stills.append(f"{still_name} (no clip selected)")
                    continue

                applied = still.ApplyToClip()
                if not applied:
                    failed_stills.append(f"{still_name} (could not apply grade)")
                    continue

                result = current_project.ExportCurrentGradeAsLUT(0, 1, lut_path)

                if result:
                    exported_count += 1
                else:
                    failed_stills.append(f"{still_name} (export failed)")

            if current_page != "color":
                resolve.OpenPage(current_page)

            if failed_stills:
                return f"Exported {exported_count} LUTs. Failed: {', '.join(failed_stills)}"
            else:
                return f"Successfully exported all {exported_count} PowerGrade LUTs"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error exporting PowerGrade LUTs: {str(e)}"

    logger.info("Registered LUT tools")
