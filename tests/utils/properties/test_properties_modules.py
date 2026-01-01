"""Tests for project properties submodules."""

from unittest.mock import Mock


class TestPropertiesModuleImports:
    """Tests that all properties submodules can be imported."""

    def test_import_properties_init(self):
        """Should import properties package with all exports."""
        from src.utils.properties import (
            get_all_project_properties,
            get_project_property,
            set_project_property,
            get_timeline_format_settings,
            set_timeline_format,
            get_superscale_settings,
            set_superscale_settings,
            get_color_settings,
            set_color_science_mode,
            set_color_space,
            get_project_metadata,
            get_project_info,
        )

        assert callable(get_all_project_properties)
        assert callable(get_project_property)
        assert callable(set_project_property)
        assert callable(get_timeline_format_settings)
        assert callable(set_timeline_format)
        assert callable(get_superscale_settings)
        assert callable(set_superscale_settings)
        assert callable(get_color_settings)
        assert callable(set_color_science_mode)
        assert callable(set_color_space)
        assert callable(get_project_metadata)
        assert callable(get_project_info)

    def test_import_core_module(self):
        """Should import core module."""
        from src.utils.properties.core import (
            get_all_project_properties,
            get_project_property,
            set_project_property,
        )

        assert callable(get_all_project_properties)
        assert callable(get_project_property)
        assert callable(set_project_property)

    def test_import_settings_module(self):
        """Should import settings module."""
        from src.utils.properties.settings import (
            get_superscale_settings,
            set_superscale_settings,
            get_color_settings,
        )

        assert callable(get_superscale_settings)
        assert callable(set_superscale_settings)
        assert callable(get_color_settings)

    def test_import_core_format_functions(self):
        """Should import format functions from core."""
        from src.utils.properties.core import (
            get_timeline_format_settings,
            set_timeline_format,
        )

        assert callable(get_timeline_format_settings)
        assert callable(set_timeline_format)


class TestGetAllProjectProperties:
    """Tests for get_all_project_properties function."""

    def test_returns_properties_dict(self):
        """Should return dictionary of properties."""
        from src.utils.properties.core import get_all_project_properties

        project = Mock()
        project.GetSetting.return_value = "test_value"

        result = get_all_project_properties(project)
        assert isinstance(result, dict)


class TestGetProjectProperty:
    """Tests for get_project_property function."""

    def test_returns_property_value(self):
        """Should return property value converted to proper type."""
        from src.utils.properties.core import get_project_property

        project = Mock()
        project.GetSetting.return_value = "1920"

        # timelineResolutionWidth is typed as int, so it gets converted
        result = get_project_property(project, "timelineResolutionWidth")
        assert result == 1920

    def test_returns_none_for_invalid_property(self):
        """Should return None for invalid property."""
        from src.utils.properties.core import get_project_property

        project = Mock()
        project.GetSetting.return_value = None

        result = get_project_property(project, "invalidProperty")
        assert result is None


class TestSetProjectProperty:
    """Tests for set_project_property function."""

    def test_returns_true_on_success(self):
        """Should return True on successful set."""
        from src.utils.properties.core import set_project_property

        project = Mock()
        project.SetSetting.return_value = True

        result = set_project_property(project, "timelineResolutionWidth", "1920")
        assert result is True

    def test_returns_false_on_failure(self):
        """Should return False on failed set."""
        from src.utils.properties.core import set_project_property

        project = Mock()
        project.SetSetting.return_value = False

        result = set_project_property(project, "invalidProperty", "value")
        assert result is False


class TestGetTimelineFormatSettings:
    """Tests for get_timeline_format_settings function."""

    def test_returns_format_dict(self):
        """Should return dictionary with format settings."""
        from src.utils.properties.settings import get_timeline_format_settings

        project = Mock()
        project.GetSetting.side_effect = lambda key: {
            "timelineResolutionWidth": "1920",
            "timelineResolutionHeight": "1080",
            "timelineFrameRate": "24",
        }.get(key)

        result = get_timeline_format_settings(project)
        assert isinstance(result, dict)


class TestSetTimelineFormat:
    """Tests for set_timeline_format function."""

    def test_returns_true_on_success(self):
        """Should return True on successful format set."""
        from src.utils.properties.core import set_timeline_format

        project = Mock()
        project.SetSetting.return_value = True

        result = set_timeline_format(project, 1920, 1080, 24.0)
        assert result is True

    def test_returns_false_on_failure(self):
        """Should return False when any setting fails."""
        from src.utils.properties.core import set_timeline_format

        project = Mock()
        project.SetSetting.return_value = False

        result = set_timeline_format(project, 1920, 1080, 24.0)
        assert result is False


class TestGetSuperscaleSettings:
    """Tests for get_superscale_settings function."""

    def test_returns_settings_dict(self):
        """Should return dictionary with superscale settings."""
        from src.utils.properties.settings import get_superscale_settings

        project = Mock()
        project.GetSetting.return_value = "1"

        result = get_superscale_settings(project)
        assert isinstance(result, dict)


class TestSetSuperscaleSettings:
    """Tests for set_superscale_settings function."""

    def test_returns_true_on_success(self):
        """Should return True on successful set."""
        from src.utils.properties.settings import set_superscale_settings

        project = Mock()
        project.SetSetting.return_value = True

        result = set_superscale_settings(project, True, 1)
        assert result is True


class TestGetColorSettings:
    """Tests for get_color_settings function."""

    def test_returns_settings_dict(self):
        """Should return dictionary with color settings."""
        from src.utils.properties.settings import get_color_settings

        project = Mock()
        project.GetSetting.return_value = "DaVinci YRGB"

        result = get_color_settings(project)
        assert isinstance(result, dict)


class TestSetColorScienceMode:
    """Tests for set_color_science_mode function."""

    def test_returns_true_on_success(self):
        """Should return True on successful set."""
        from src.utils.properties.settings import set_color_science_mode

        project = Mock()
        project.SetSetting.return_value = True

        result = set_color_science_mode(project, "DaVinci YRGB")
        assert result is True


class TestSetColorSpace:
    """Tests for set_color_space function."""

    def test_returns_true_on_success(self):
        """Should return True on successful set."""
        from src.utils.properties.settings import set_color_space

        project = Mock()
        project.SetSetting.return_value = True

        result = set_color_space(project, "Rec.709", "Rec.709 Gamma")
        assert result is True


class TestGetProjectMetadata:
    """Tests for get_project_metadata function."""

    def test_returns_metadata_dict(self):
        """Should return dictionary with metadata."""
        from src.utils.properties.settings import get_project_metadata

        project = Mock()
        project.GetName.return_value = "TestProject"

        result = get_project_metadata(project)
        assert isinstance(result, dict)


class TestGetProjectInfo:
    """Tests for get_project_info function."""

    def test_returns_info_dict(self):
        """Should return dictionary with project info."""
        from src.utils.properties.settings import get_project_info

        project = Mock()
        project.GetName.return_value = "TestProject"
        project.GetSetting.return_value = "value"

        result = get_project_info(project)
        assert isinstance(result, dict)
