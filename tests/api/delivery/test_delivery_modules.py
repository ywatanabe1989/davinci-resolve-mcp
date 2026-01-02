"""Tests for delivery operations submodules."""

from unittest.mock import Mock


class TestDeliveryModuleImports:
    """Tests that all delivery submodules can be imported."""

    def test_import_delivery_init(self):
        """Should import delivery package with all exports."""
        from src.api.delivery import (
            get_render_presets,
            add_to_render_queue,
            ensure_deliver_page,
            validate_render_preset,
            start_render,
            get_render_queue_status,
            clear_render_queue,
        )

        assert callable(get_render_presets)
        assert callable(add_to_render_queue)
        assert callable(ensure_deliver_page)
        assert callable(validate_render_preset)
        assert callable(start_render)
        assert callable(get_render_queue_status)
        assert callable(clear_render_queue)

    def test_import_render_module(self):
        """Should import render module."""
        from src.api.delivery.render import get_render_presets, add_to_render_queue

        assert callable(get_render_presets)
        assert callable(add_to_render_queue)

    def test_import_queue_module(self):
        """Should import queue module."""
        from src.api.delivery.queue import (
            start_render,
            get_render_queue_status,
            clear_render_queue,
        )

        assert callable(start_render)
        assert callable(get_render_queue_status)
        assert callable(clear_render_queue)


class TestGetRenderPresets:
    """Tests for get_render_presets function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.delivery.render import get_render_presets

        result = get_render_presets(None)
        # Returns dict with error key on failure
        assert isinstance(result, dict)
        assert "error" in result

    def test_returns_error_when_no_project(self):
        """Should return error when no project open."""
        from src.api.delivery.render import get_render_presets

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = get_render_presets(resolve)
        # Returns dict with error key on failure
        assert isinstance(result, dict)
        assert "error" in result


class TestAddToRenderQueue:
    """Tests for add_to_render_queue function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.delivery.render import add_to_render_queue

        result = add_to_render_queue(None, "preset_name")
        # Returns dict with error key
        assert isinstance(result, dict)
        assert "error" in result


class TestStartRender:
    """Tests for start_render function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.delivery.queue import start_render

        result = start_render(None)
        # Returns dict with error key
        assert isinstance(result, dict)
        assert "error" in result


class TestGetRenderQueueStatus:
    """Tests for get_render_queue_status function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.delivery.queue import get_render_queue_status

        result = get_render_queue_status(None)
        assert "error" in result


class TestClearRenderQueue:
    """Tests for clear_render_queue function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.delivery.queue import clear_render_queue

        result = clear_render_queue(None)
        # Returns dict with error key
        assert isinstance(result, dict)
        assert "error" in result
