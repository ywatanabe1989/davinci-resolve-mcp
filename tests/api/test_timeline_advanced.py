"""Tests for timeline advanced operations module."""

from unittest.mock import Mock


class TestDuplicateTimeline:
    """Tests for duplicate_timeline function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import duplicate_timeline

        result = duplicate_timeline(None)
        assert "Error" in result

    def test_returns_error_when_no_project_open(self):
        """Should return error when no project is open."""
        from src.api.timeline_advanced import duplicate_timeline

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = duplicate_timeline(resolve)
        assert "Error" in result

    def test_duplicates_current_timeline_on_success(self):
        """Should duplicate current timeline when no name specified."""
        from src.api.timeline_advanced import duplicate_timeline

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        media_pool = Mock()
        timeline = Mock()
        new_timeline = Mock()

        timeline.GetName.return_value = "OriginalTimeline"
        new_timeline.GetName.return_value = "OriginalTimeline_copy"
        project.GetCurrentTimeline.return_value = timeline
        media_pool.DuplicateTimeline.return_value = new_timeline
        project.GetMediaPool.return_value = media_pool
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = duplicate_timeline(resolve)
        assert "Duplicated" in result or "copy" in result


class TestCreateCompoundClip:
    """Tests for create_compound_clip function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import create_compound_clip

        result = create_compound_clip(None, ["clip1", "clip2"])
        assert "Error" in result

    def test_returns_error_for_empty_clip_names(self):
        """Should return error for empty clip names list."""
        from src.api.timeline_advanced import create_compound_clip

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = create_compound_clip(resolve, [])
        assert "Error" in result


class TestCreateFusionClip:
    """Tests for create_fusion_clip function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import create_fusion_clip

        result = create_fusion_clip(None, ["clip1"])
        assert "Error" in result

    def test_returns_error_for_empty_clip_names(self):
        """Should return error for empty clip names list."""
        from src.api.timeline_advanced import create_fusion_clip

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = create_fusion_clip(resolve, [])
        assert "Error" in result


class TestInsertGenerator:
    """Tests for insert_generator function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import insert_generator

        result = insert_generator(None, "Solid Color")
        assert "Error" in result

    def test_returns_error_for_empty_generator_name(self):
        """Should return error for empty generator name."""
        from src.api.timeline_advanced import insert_generator

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = insert_generator(resolve, "")
        assert "Error" in result


class TestInsertTitle:
    """Tests for insert_title function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import insert_title

        result = insert_title(None, "Text+")
        assert "Error" in result

    def test_returns_error_for_empty_title_name(self):
        """Should return error for empty title name."""
        from src.api.timeline_advanced import insert_title

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = insert_title(resolve, "")
        assert "Error" in result


class TestInsertFusionComposition:
    """Tests for insert_fusion_composition function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.timeline_advanced import insert_fusion_composition

        result = insert_fusion_composition(None)
        assert "Error" in result

    def test_returns_error_when_no_timeline(self):
        """Should return error when no timeline active."""
        from src.api.timeline_advanced import insert_fusion_composition

        resolve = Mock()
        project_manager = Mock()
        project = Mock()
        project.GetCurrentTimeline.return_value = None
        project_manager.GetCurrentProject.return_value = project
        resolve.GetProjectManager.return_value = project_manager

        result = insert_fusion_composition(resolve)
        assert "Error" in result
