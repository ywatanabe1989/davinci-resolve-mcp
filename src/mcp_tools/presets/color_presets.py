#!/usr/bin/env python3
"""
DaVinci Resolve MCP Color Preset Tools
Color preset management in gallery
"""

from typing import List, Dict, Any


def register_color_preset_tools(mcp, resolve, logger):
    """Register color preset MCP tools and resources."""

    @mcp.resource("resolve://color/presets")
    def get_color_presets() -> List[Dict[str, Any]]:
        """Get all available color presets in the current project."""
        if resolve is None:
            return [{"error": "Not connected to DaVinci Resolve"}]

        project_manager = resolve.GetProjectManager()
        if not project_manager:
            return [{"error": "Failed to get Project Manager"}]

        current_project = project_manager.GetCurrentProject()
        if not current_project:
            return [{"error": "No project currently open"}]

        current_page = resolve.GetCurrentPage()
        if current_page != "color":
            resolve.OpenPage("color")

        try:
            gallery = current_project.GetGallery()
            if not gallery:
                return [{"error": "Failed to get gallery"}]

            albums = gallery.GetAlbums()
            if not albums:
                return [{"info": "No albums found in gallery"}]

            result = []
            for album in albums:
                stills = album.GetStills()
                album_info = {"name": album.GetName(), "stills": []}

                if stills:
                    for still in stills:
                        still_info = {
                            "id": still.GetUniqueId(),
                            "label": still.GetLabel(),
                            "timecode": still.GetTimecode(),
                            "isGrabbed": still.IsGrabbed(),
                        }
                        album_info["stills"].append(still_info)

                result.append(album_info)

            if current_page != "color":
                resolve.OpenPage(current_page)

            return result

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return [{"error": f"Error retrieving color presets: {str(e)}"}]

    @mcp.tool()
    def save_color_preset(
        clip_name: str = None,
        preset_name: str = None,
        album_name: str = "DaVinci Resolve",
    ) -> str:
        """Save a color preset from the specified clip."""
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

            gallery = current_project.GetGallery()
            if not gallery:
                return "Error: Failed to get gallery"

            album = None
            albums = gallery.GetAlbums()
            if albums:
                for a in albums:
                    if a.GetName() == album_name:
                        album = a
                        break

            if not album:
                album = gallery.CreateAlbum(album_name)
                if not album:
                    return f"Error: Failed to create album '{album_name}'"

            final_preset_name = preset_name
            if not final_preset_name:
                if clip_name:
                    final_preset_name = f"{clip_name} Preset"
                else:
                    current_clip = current_timeline.GetCurrentVideoItem()
                    if current_clip:
                        final_preset_name = f"{current_clip.GetName()} Preset"
                    else:
                        final_preset_name = f"Preset {len(album.GetStills()) + 1}"

            result = gallery.GrabStill()

            if not result:
                return "Error: Failed to grab still for the preset"

            stills = album.GetStills()
            if stills:
                latest_still = stills[-1]
                latest_still.SetLabel(final_preset_name)

            if current_page != "color":
                resolve.OpenPage(current_page)

            return f"Successfully saved color preset '{final_preset_name}'"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error saving color preset: {str(e)}"

    @mcp.tool()
    def apply_color_preset(
        preset_id: str = None,
        preset_name: str = None,
        clip_name: str = None,
        album_name: str = "DaVinci Resolve",
    ) -> str:
        """Apply a color preset to the specified clip."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        if not preset_id and not preset_name:
            return "Error: Must provide either preset_id or preset_name"

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

            gallery = current_project.GetGallery()
            if not gallery:
                return "Error: Failed to get gallery"

            album = None
            albums = gallery.GetAlbums()
            if albums:
                for a in albums:
                    if a.GetName() == album_name:
                        album = a
                        break

            if not album:
                return f"Error: Album '{album_name}' not found"

            stills = album.GetStills()
            if not stills:
                return f"Error: No presets found in album '{album_name}'"

            target_still = None
            if preset_id:
                for still in stills:
                    if still.GetUniqueId() == preset_id:
                        target_still = still
                        break
            elif preset_name:
                for still in stills:
                    if still.GetLabel() == preset_name:
                        target_still = still
                        break

            if not target_still:
                return f"Error: Preset not found in album '{album_name}'"

            result = target_still.ApplyToClip()

            if current_page != "color":
                resolve.OpenPage(current_page)

            if result:
                return "Successfully applied color preset"
            else:
                return "Failed to apply color preset"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error applying color preset: {str(e)}"

    @mcp.tool()
    def delete_color_preset(
        preset_id: str = None,
        preset_name: str = None,
        album_name: str = "DaVinci Resolve",
    ) -> str:
        """Delete a color preset."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        if not preset_id and not preset_name:
            return "Error: Must provide either preset_id or preset_name"

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

            album = None
            albums = gallery.GetAlbums()
            if albums:
                for a in albums:
                    if a.GetName() == album_name:
                        album = a
                        break

            if not album:
                return f"Error: Album '{album_name}' not found"

            stills = album.GetStills()
            if not stills:
                return f"Error: No presets found in album '{album_name}'"

            target_still = None
            if preset_id:
                for still in stills:
                    if still.GetUniqueId() == preset_id:
                        target_still = still
                        break
            elif preset_name:
                for still in stills:
                    if still.GetLabel() == preset_name:
                        target_still = still
                        break

            if not target_still:
                return f"Error: Preset not found in album '{album_name}'"

            result = album.DeleteStill(target_still)

            if current_page != "color":
                resolve.OpenPage(current_page)

            if result:
                return "Successfully deleted color preset"
            else:
                return "Failed to delete color preset"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error deleting color preset: {str(e)}"

    @mcp.tool()
    def create_color_preset_album(album_name: str) -> str:
        """Create a new album for color presets."""
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

            albums = gallery.GetAlbums()
            if albums:
                for a in albums:
                    if a.GetName() == album_name:
                        if current_page != "color":
                            resolve.OpenPage(current_page)
                        return f"Album '{album_name}' already exists"

            album = gallery.CreateAlbum(album_name)

            if current_page != "color":
                resolve.OpenPage(current_page)

            if album:
                return f"Successfully created album '{album_name}'"
            else:
                return f"Failed to create album '{album_name}'"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error creating album: {str(e)}"

    @mcp.tool()
    def delete_color_preset_album(album_name: str) -> str:
        """Delete a color preset album."""
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

            album = None
            albums = gallery.GetAlbums()
            if albums:
                for a in albums:
                    if a.GetName() == album_name:
                        album = a
                        break

            if not album:
                if current_page != "color":
                    resolve.OpenPage(current_page)
                return f"Error: Album '{album_name}' not found"

            result = gallery.DeleteAlbum(album)

            if current_page != "color":
                resolve.OpenPage(current_page)

            if result:
                return f"Successfully deleted album '{album_name}'"
            else:
                return f"Failed to delete album '{album_name}'"

        except Exception as e:
            if current_page != "color":
                resolve.OpenPage(current_page)
            return f"Error deleting album: {str(e)}"

    logger.info("Registered color preset tools")
