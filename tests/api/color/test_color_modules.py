"""Tests for color operations submodules."""

from unittest.mock import Mock


class TestColorModuleImports:
    """Tests that all color submodules can be imported."""

    def test_import_color_init(self):
        """Should import color package with all exports."""
        from src.api.color import (
            get_current_node,
            add_node,
            ensure_clip_selected,
            apply_lut,
            copy_grade,
            get_color_wheels,
            set_color_wheel_param,
        )

        assert callable(get_current_node)
        assert callable(add_node)
        assert callable(ensure_clip_selected)
        assert callable(apply_lut)
        assert callable(copy_grade)
        assert callable(get_color_wheels)
        assert callable(set_color_wheel_param)

    def test_import_nodes_module(self):
        """Should import nodes module."""
        from src.api.color.nodes import get_current_node, add_node

        assert callable(get_current_node)
        assert callable(add_node)

    def test_import_grades_module(self):
        """Should import grades module."""
        from src.api.color.grades import apply_lut, copy_grade

        assert callable(apply_lut)
        assert callable(copy_grade)

    def test_import_wheels_module(self):
        """Should import wheels module."""
        from src.api.color.wheels import get_color_wheels, set_color_wheel_param

        assert callable(get_color_wheels)
        assert callable(set_color_wheel_param)


class TestGetCurrentNode:
    """Tests for get_current_node function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.nodes import get_current_node

        result = get_current_node(None)
        assert "error" in result

    def test_returns_error_when_no_project(self):
        """Should return error when no project open."""
        from src.api.color.nodes import get_current_node

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = get_current_node(resolve)
        assert "error" in result


class TestAddNode:
    """Tests for add_node function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.nodes import add_node

        result = add_node(None)
        assert "error" in result.lower()

    def test_returns_error_when_no_project(self):
        """Should return error when no project open."""
        from src.api.color.nodes import add_node

        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager

        result = add_node(resolve)
        assert "error" in result.lower()


class TestApplyLut:
    """Tests for apply_lut function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.grades import apply_lut

        result = apply_lut(None, "/path/to/lut.cube")
        assert "error" in result.lower()


class TestCopyGrade:
    """Tests for copy_grade function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.grades import copy_grade

        result = copy_grade(None)
        assert "error" in result.lower()


class TestGetColorWheels:
    """Tests for get_color_wheels function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.wheels import get_color_wheels

        result = get_color_wheels(None)
        assert "error" in result


class TestSetColorWheelParam:
    """Tests for set_color_wheel_param function."""

    def test_returns_error_when_resolve_is_none(self):
        """Should return error when not connected."""
        from src.api.color.wheels import set_color_wheel_param

        result = set_color_wheel_param(None, "lift", "red", 0.0)
        assert "error" in result.lower()
