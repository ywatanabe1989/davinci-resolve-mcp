"""Tests for timeline operations submodules."""

from unittest.mock import Mock


class TestTimelineModuleImports:
    """Tests that all timeline submodules can be imported."""

    def test_import_timeline_init(self):
        """Should import timeline package with all exports."""
        from src.api.timeline import (
            list_timelines,
            get_current_timeline_info,
            create_timeline,
            create_empty_timeline,
            set_current_timeline,
            delete_timeline,
            get_timeline_tracks,
            add_marker,
        )

        assert callable(list_timelines)
        assert callable(get_current_timeline_info)
        assert callable(create_timeline)
        assert callable(create_empty_timeline)
        assert callable(set_current_timeline)
        assert callable(delete_timeline)
        assert callable(get_timeline_tracks)
        assert callable(add_marker)

    def test_import_basic_module(self):
        """Should import basic module."""
        from src.api.timeline.basic import list_timelines, create_timeline

        assert callable(list_timelines)
        assert callable(create_timeline)

    def test_import_markers_module(self):
        """Should import markers module."""
        from src.api.timeline.markers import add_marker

        assert callable(add_marker)


class TestListTimelines:
    """Tests for list_timelines function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import list_timelines

        result = list_timelines(None)
        assert isinstance(result, list)
        assert "error" in result[0].lower()

    def test_returns_error_when_no_project(self):
        """Should return error when no project open."""
        from src.api.timeline.basic import list_timelines

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = list_timelines(resolve)
        assert isinstance(result, list)
        assert "error" in result[0].lower()


class TestGetCurrentTimelineInfo:
    """Tests for get_current_timeline_info function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import get_current_timeline_info

        result = get_current_timeline_info(None)
        assert "error" in result


class TestCreateTimeline:
    """Tests for create_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import create_timeline

        result = create_timeline(None, "New Timeline")
        assert "error" in result.lower()


class TestSetCurrentTimeline:
    """Tests for set_current_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import set_current_timeline

        result = set_current_timeline(None, "Timeline Name")
        assert "error" in result.lower()


class TestDeleteTimeline:
    """Tests for delete_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import delete_timeline

        result = delete_timeline(None, "Timeline Name")
        assert "error" in result.lower()


class TestGetTimelineTracks:
    """Tests for get_timeline_tracks function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.basic import get_timeline_tracks

        result = get_timeline_tracks(None)
        assert "error" in result


class TestAddMarker:
    """Tests for add_marker function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline.markers import add_marker

        result = add_marker(None)
        assert "error" in result.lower()
