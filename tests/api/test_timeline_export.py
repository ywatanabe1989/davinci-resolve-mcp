"""Tests for timeline export operations module."""

from unittest.mock import Mock


class TestImportTimelineFromFile:
    """Tests for import_timeline_from_file function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import import_timeline_from_file

        result = import_timeline_from_file(None, "/path/to/file.aaf")
        assert "Error" in result

    def test_returns_error_for_empty_file_path(self):
        """Should return error for empty file path."""
        from src.api.timeline_export import import_timeline_from_file

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = import_timeline_from_file(resolve, "")
        assert "Error" in result


class TestExportTimeline:
    """Tests for export_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import export_timeline

        result = export_timeline(None, "/path/to/output.aaf", "AAF")
        assert "Error" in result

    def test_returns_error_for_empty_file_path(self):
        """Should return error for empty file path."""
        from src.api.timeline_export import export_timeline

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = export_timeline(resolve, "", "AAF")
        assert "Error" in result

    def test_returns_error_for_invalid_export_type(self):
        """Should return error for invalid export type."""
        from src.api.timeline_export import export_timeline

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = export_timeline(resolve, "/output.xyz", "INVALID_TYPE")
        assert "Error" in result


class TestGetTimelineTimecode:
    """Tests for get_timeline_timecode function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import get_timeline_timecode

        result = get_timeline_timecode(None)
        assert "Error" in result

    def test_returns_timecode_on_success(self):
        """Should return current timecode."""
        from src.api.timeline_export import get_timeline_timecode

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        timeline.GetCurrentTimecode.return_value = "01:00:00:00"
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_timeline_timecode(resolve)
        assert "01:00:00:00" in result


class TestSetTimelineTimecode:
    """Tests for set_timeline_timecode function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import set_timeline_timecode

        result = set_timeline_timecode(None, "01:00:00:00")
        assert "Error" in result

    def test_returns_error_for_empty_timecode(self):
        """Should return error for empty timecode."""
        from src.api.timeline_export import set_timeline_timecode

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = set_timeline_timecode(resolve, "")
        assert "Error" in result


class TestDetectSceneCuts:
    """Tests for detect_scene_cuts function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import detect_scene_cuts

        result = detect_scene_cuts(None)
        assert "Error" in result

    def test_returns_error_when_no_timeline(self):
        """Should return error when no timeline active."""
        from src.api.timeline_export import detect_scene_cuts

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = None
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = detect_scene_cuts(resolve)
        assert "Error" in result


class TestCreateSubtitlesFromAudio:
    """Tests for create_subtitles_from_audio function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import create_subtitles_from_audio

        result = create_subtitles_from_audio(None)
        assert "Error" in result


class TestExportCurrentFrameAsStill:
    """Tests for export_current_frame_as_still function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_export import export_current_frame_as_still

        result = export_current_frame_as_still(None, "/path/to/still.png")
        assert "Error" in result

    def test_returns_error_for_empty_file_path(self):
        """Should return error for empty file path."""
        from src.api.timeline_export import export_current_frame_as_still

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = export_current_frame_as_still(resolve, "")
        assert "Error" in result
