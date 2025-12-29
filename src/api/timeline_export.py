"""
Timeline Export/Import Operations for DaVinci Resolve MCP Server.

Implements timeline import/export, timecode, and subtitle generation.
"""


def import_timeline_from_file(
    resolve,
    file_path: str,
    timeline_name: str = None,
    import_source_clips: bool = True,
    source_clips_path: str = None,
) -> str:
    """Import a timeline from file (AAF/EDL/XML/FCPXML/DRT/ADL/OTIO)."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not file_path:
        return "Error: File path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        media_pool = current_project.GetMediaPool()
        if not media_pool:
            return "Error: Failed to get Media Pool"

        import_options = {"importSourceClips": import_source_clips}
        if timeline_name:
            import_options["timelineName"] = timeline_name
        if source_clips_path:
            import_options["sourceClipsPath"] = source_clips_path

        result = media_pool.ImportTimelineFromFile(file_path, import_options)
        if result:
            return f"Imported timeline from '{file_path}'"
        return f"Failed to import timeline from '{file_path}'"
    except Exception as e:
        return f"Error: {str(e)}"


EXPORT_TYPES = {
    "AAF": "EXPORT_AAF",
    "DRT": "EXPORT_DRT",
    "EDL": "EXPORT_EDL",
    "FCP_7_XML": "EXPORT_FCP_7_XML",
    "FCPXML_1_8": "EXPORT_FCPXML_1_8",
    "FCPXML_1_9": "EXPORT_FCPXML_1_9",
    "FCPXML_1_10": "EXPORT_FCPXML_1_10",
    "HDR_10_PROFILE_A": "EXPORT_HDR_10_PROFILE_A",
    "HDR_10_PROFILE_B": "EXPORT_HDR_10_PROFILE_B",
    "TEXT_CSV": "EXPORT_TEXT_CSV",
    "TEXT_TAB": "EXPORT_TEXT_TAB",
    "DOLBY_VISION_VER_2_9": "EXPORT_DOLBY_VISION_VER_2_9",
    "DOLBY_VISION_VER_4_0": "EXPORT_DOLBY_VISION_VER_4_0",
    "DOLBY_VISION_VER_5_1": "EXPORT_DOLBY_VISION_VER_5_1",
    "OTIO": "EXPORT_OTIO",
    "ALE": "EXPORT_ALE",
    "ALE_CDL": "EXPORT_ALE_CDL",
}

EXPORT_SUBTYPES = {
    "NONE": "EXPORT_NONE",
    "AAF_NEW": "EXPORT_AAF_NEW",
    "AAF_EXISTING": "EXPORT_AAF_EXISTING",
    "CDL": "EXPORT_CDL",
    "SDL": "EXPORT_SDL",
    "MISSING_CLIPS": "EXPORT_MISSING_CLIPS",
}


def export_timeline(
    resolve, file_path: str, export_type: str, export_subtype: str = "NONE"
) -> str:
    """Export the current timeline."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not file_path or not export_type:
        return "Error: File path and export type are required"

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
        if export_type.upper() not in EXPORT_TYPES:
            return f"Error: Invalid export type. Use: {', '.join(EXPORT_TYPES.keys())}"
        if export_subtype.upper() not in EXPORT_SUBTYPES:
            types = ", ".join(EXPORT_SUBTYPES.keys())
            return f"Error: Invalid export subtype. Use: {types}"

        type_const = getattr(resolve, EXPORT_TYPES[export_type.upper()], None)
        subtype_const = getattr(resolve, EXPORT_SUBTYPES[export_subtype.upper()], None)

        if type_const is None:
            type_const = EXPORT_TYPES[export_type.upper()]
        if subtype_const is None:
            subtype_const = EXPORT_SUBTYPES[export_subtype.upper()]

        result = current_timeline.Export(file_path, type_const, subtype_const)
        if result:
            return f"Exported timeline to '{file_path}'"
        return f"Failed to export timeline to '{file_path}'"
    except Exception as e:
        return f"Error: {str(e)}"


def get_timeline_timecode(resolve) -> str:
    """Get the current playhead timecode."""
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
        timecode = current_timeline.GetCurrentTimecode()
        return timecode if timecode else "Unable to get timecode"
    except Exception as e:
        return f"Error: {str(e)}"


def set_timeline_timecode(resolve, timecode: str) -> str:
    """Set the playhead to a specific timecode."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not timecode:
        return "Error: Timecode cannot be empty"

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
        result = current_timeline.SetCurrentTimecode(timecode)
        if result:
            return f"Set timecode to '{timecode}'"
        return f"Failed to set timecode to '{timecode}'"
    except Exception as e:
        return f"Error: {str(e)}"


def detect_scene_cuts(resolve) -> str:
    """Detect and create scene cuts along the timeline."""
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
        result = current_timeline.DetectSceneCuts()
        if result:
            return "Detected and created scene cuts"
        return "Failed to detect scene cuts"
    except Exception as e:
        return f"Error: {str(e)}"


LANGUAGE_MAP = {
    "auto": "AUTO_CAPTION_AUTO",
    "danish": "AUTO_CAPTION_DANISH",
    "dutch": "AUTO_CAPTION_DUTCH",
    "english": "AUTO_CAPTION_ENGLISH",
    "french": "AUTO_CAPTION_FRENCH",
    "german": "AUTO_CAPTION_GERMAN",
    "italian": "AUTO_CAPTION_ITALIAN",
    "japanese": "AUTO_CAPTION_JAPANESE",
    "korean": "AUTO_CAPTION_KOREAN",
    "mandarin_simplified": "AUTO_CAPTION_MANDARIN_SIMPLIFIED",
    "mandarin_traditional": "AUTO_CAPTION_MANDARIN_TRADITIONAL",
    "norwegian": "AUTO_CAPTION_NORWEGIAN",
    "portuguese": "AUTO_CAPTION_PORTUGUESE",
    "russian": "AUTO_CAPTION_RUSSIAN",
    "spanish": "AUTO_CAPTION_SPANISH",
    "swedish": "AUTO_CAPTION_SWEDISH",
}


def create_subtitles_from_audio(
    resolve, language: str = None, chars_per_line: int = None
) -> str:
    """Create subtitles from audio for the timeline."""
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
        settings = {}
        if language and language.lower() in LANGUAGE_MAP:
            lang_const = getattr(resolve, LANGUAGE_MAP[language.lower()], None)
            if lang_const and hasattr(resolve, "SUBTITLE_LANGUAGE"):
                settings[resolve.SUBTITLE_LANGUAGE] = lang_const

        if chars_per_line and 1 <= chars_per_line <= 60:
            if hasattr(resolve, "SUBTITLE_CHARS_PER_LINE"):
                settings[resolve.SUBTITLE_CHARS_PER_LINE] = chars_per_line

        if settings:
            result = current_timeline.CreateSubtitlesFromAudio(settings)
        else:
            result = current_timeline.CreateSubtitlesFromAudio()

        if result:
            return "Started subtitle creation from audio"
        return "Failed to create subtitles from audio"
    except Exception as e:
        return f"Error: {str(e)}"


def export_current_frame_as_still(resolve, file_path: str) -> str:
    """Export the current frame as a still image."""
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    if not file_path:
        return "Error: File path cannot be empty"

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"

    try:
        result = current_project.ExportCurrentFrameAsStill(file_path)
        if result:
            return f"Exported current frame to '{file_path}'"
        return f"Failed to export frame to '{file_path}'"
    except Exception as e:
        return f"Error: {str(e)}"
