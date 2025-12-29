"""Tests for marker operations module."""

from unittest.mock import Mock


class TestGetTimelineMarkers:
    """Tests for get_timeline_markers function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import get_timeline_markers

        result = get_timeline_markers(None)
        assert "error" in result

    def test_returns_error_when_no_timeline(self):
        """Should return error when no timeline active."""
        from src.api.marker_operations import get_timeline_markers

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = None
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_timeline_markers(resolve)
        assert "error" in result

    def test_returns_markers_on_success(self):
        """Should return markers from timeline."""
        from src.api.marker_operations import get_timeline_markers

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()

        markers = {
            100: {"color": "Blue", "name": "Marker1"},
            200: {"color": "Red", "name": "Marker2"},
        }
        timeline.GetMarkers.return_value = markers
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_timeline_markers(resolve)
        assert "markers" in result
        assert result["count"] == 2


class TestAddTimelineMarker:
    """Tests for add_timeline_marker function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import add_timeline_marker

        result = add_timeline_marker(None, 100)
        assert "Error" in result

    def test_returns_error_for_invalid_color(self):
        """Should return error for invalid marker color."""
        from src.api.marker_operations import add_timeline_marker

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = add_timeline_marker(resolve, 100, color="InvalidColor")
        assert "Error" in result
        assert "Invalid color" in result

    def test_adds_marker_on_success(self):
        """Should add marker to timeline."""
        from src.api.marker_operations import add_timeline_marker

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        timeline.AddMarker.return_value = True
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = add_timeline_marker(resolve, 100, color="Blue", name="TestMarker")
        assert "Added" in result


class TestDeleteTimelineMarkerAtFrame:
    """Tests for delete_timeline_marker_at_frame function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import delete_timeline_marker_at_frame

        result = delete_timeline_marker_at_frame(None, 100)
        assert "Error" in result

    def test_deletes_marker_on_success(self):
        """Should delete marker at frame."""
        from src.api.marker_operations import delete_timeline_marker_at_frame

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        timeline.DeleteMarkerAtFrame.return_value = True
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = delete_timeline_marker_at_frame(resolve, 100)
        assert "Deleted" in result


class TestDeleteTimelineMarkersByColor:
    """Tests for delete_timeline_markers_by_color function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import delete_timeline_markers_by_color

        result = delete_timeline_markers_by_color(None, "Blue")
        assert "Error" in result

    def test_deletes_markers_on_success(self):
        """Should delete all markers of specified color."""
        from src.api.marker_operations import delete_timeline_markers_by_color

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        timeline = Mock()
        timeline.DeleteMarkersByColor.return_value = True
        project.GetCurrentTimeline.return_value = timeline
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = delete_timeline_markers_by_color(resolve, "Blue")
        assert "Deleted" in result


class TestGetMarkerByCustomData:
    """Tests for get_marker_by_custom_data function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import get_marker_by_custom_data

        result = get_marker_by_custom_data(None, "custom_id_123")
        assert "error" in result

    def test_returns_error_for_empty_custom_data(self):
        """Should return error for empty custom data."""
        from src.api.marker_operations import get_marker_by_custom_data

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_marker_by_custom_data(resolve, "")
        assert "error" in result


class TestGetClipMarkers:
    """Tests for get_clip_markers function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import get_clip_markers

        result = get_clip_markers(None, "MyClip")
        assert "error" in result

    def test_returns_error_for_empty_clip_name(self):
        """Should return error for empty clip name."""
        from src.api.marker_operations import get_clip_markers

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = get_clip_markers(resolve, "")
        assert "error" in result


class TestAddClipMarker:
    """Tests for add_clip_marker function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.marker_operations import add_clip_marker

        result = add_clip_marker(None, "MyClip", 100)
        assert "Error" in result

    def test_returns_error_for_empty_clip_name(self):
        """Should return error for empty clip name."""
        from src.api.marker_operations import add_clip_marker

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = add_clip_marker(resolve, "", 100)
        assert "Error" in result
