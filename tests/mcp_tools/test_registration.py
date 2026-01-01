"""Tests for MCP tools registration functions."""

from unittest.mock import Mock, MagicMock


class TestModuleImports:
    """Tests that all MCP tool modules can be imported."""

    def test_import_mcp_tools_init(self):
        """Should import mcp_tools package."""
        from src.mcp_tools import register_all_tools

        assert callable(register_all_tools)

    def test_import_core_tools(self):
        """Should import core tools module."""
        from src.mcp_tools.core import register_core_tools

        assert callable(register_core_tools)

    def test_import_project_tools(self):
        """Should import project tools module."""
        from src.mcp_tools.project import register_project_tools

        assert callable(register_project_tools)

    def test_import_timeline_tools(self):
        """Should import timeline tools module."""
        from src.mcp_tools.timeline import register_timeline_tools

        assert callable(register_timeline_tools)

    def test_import_media_tools(self):
        """Should import media tools module."""
        from src.mcp_tools.media import register_media_tools

        assert callable(register_media_tools)

    def test_import_color_tools(self):
        """Should import color tools module."""
        from src.mcp_tools.color import register_color_tools

        assert callable(register_color_tools)

    def test_import_delivery_tools(self):
        """Should import delivery tools module."""
        from src.mcp_tools.delivery import register_delivery_tools

        assert callable(register_delivery_tools)

    def test_import_cache_tools(self):
        """Should import cache tools module."""
        from src.mcp_tools.cache import register_cache_tools

        assert callable(register_cache_tools)

    def test_import_keyframe_tools(self):
        """Should import keyframe tools module."""
        from src.mcp_tools.keyframes import register_keyframe_tools

        assert callable(register_keyframe_tools)

    def test_import_preset_tools(self):
        """Should import preset tools module."""
        from src.mcp_tools.presets import register_preset_tools

        assert callable(register_preset_tools)

    def test_import_inspection_tools(self):
        """Should import inspection tools module."""
        from src.mcp_tools.inspection import register_inspection_tools

        assert callable(register_inspection_tools)

    def test_import_layout_tools(self):
        """Should import layout tools module."""
        from src.mcp_tools.layout import register_layout_tools

        assert callable(register_layout_tools)

    def test_import_app_tools(self):
        """Should import app tools module."""
        from src.mcp_tools.app import register_app_tools

        assert callable(register_app_tools)

    def test_import_cloud_tools(self):
        """Should import cloud tools module."""
        from src.mcp_tools.cloud import register_cloud_tools

        assert callable(register_cloud_tools)

    def test_import_property_tools(self):
        """Should import property tools module."""
        from src.mcp_tools.properties import register_property_tools

        assert callable(register_property_tools)

    def test_import_timeline_item_tools(self):
        """Should import timeline item tools module."""
        from src.mcp_tools.timeline_items import register_timeline_item_tools

        assert callable(register_timeline_item_tools)


class TestRegisterAllTools:
    """Tests for register_all_tools function."""

    def test_registers_all_tool_modules(self):
        """Should call all registration functions."""
        from src.mcp_tools import register_all_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        # Should not raise any exceptions
        register_all_tools(mcp, resolve, logger)

        # Verify logger was called for each module
        assert logger.info.call_count >= 15


class TestCoreToolsRegistration:
    """Tests for core tools registration."""

    def test_registers_without_error(self):
        """Should register core tools without error."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_core_tools(mcp, resolve, logger)

        # Verify decorators were called
        assert mcp.resource.called or mcp.tool.called
        logger.info.assert_called()


class TestProjectToolsRegistration:
    """Tests for project tools registration."""

    def test_registers_without_error(self):
        """Should register project tools without error."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_project_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestTimelineToolsRegistration:
    """Tests for timeline tools registration."""

    def test_registers_without_error(self):
        """Should register timeline tools without error."""
        from src.mcp_tools.timeline import register_timeline_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_timeline_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestMediaToolsRegistration:
    """Tests for media tools registration."""

    def test_registers_without_error(self):
        """Should register media tools without error."""
        from src.mcp_tools.media import register_media_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_media_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestColorToolsRegistration:
    """Tests for color tools registration."""

    def test_registers_without_error(self):
        """Should register color tools without error."""
        from src.mcp_tools.color import register_color_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_color_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestDeliveryToolsRegistration:
    """Tests for delivery tools registration."""

    def test_registers_without_error(self):
        """Should register delivery tools without error."""
        from src.mcp_tools.delivery import register_delivery_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_delivery_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestCacheToolsRegistration:
    """Tests for cache tools registration."""

    def test_registers_without_error(self):
        """Should register cache tools without error."""
        from src.mcp_tools.cache import register_cache_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_cache_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestKeyframeToolsRegistration:
    """Tests for keyframe tools registration."""

    def test_registers_without_error(self):
        """Should register keyframe tools without error."""
        from src.mcp_tools.keyframes import register_keyframe_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_keyframe_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestPresetToolsRegistration:
    """Tests for preset tools registration."""

    def test_registers_without_error(self):
        """Should register preset tools without error."""
        from src.mcp_tools.presets import register_preset_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_preset_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestInspectionToolsRegistration:
    """Tests for inspection tools registration."""

    def test_registers_without_error(self):
        """Should register inspection tools without error."""
        from src.mcp_tools.inspection import register_inspection_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_inspection_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestLayoutToolsRegistration:
    """Tests for layout tools registration."""

    def test_registers_without_error(self):
        """Should register layout tools without error."""
        from src.mcp_tools.layout import register_layout_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_layout_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestAppToolsRegistration:
    """Tests for app tools registration."""

    def test_registers_without_error(self):
        """Should register app tools without error."""
        from src.mcp_tools.app import register_app_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_app_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestCloudToolsRegistration:
    """Tests for cloud tools registration."""

    def test_registers_without_error(self):
        """Should register cloud tools without error."""
        from src.mcp_tools.cloud import register_cloud_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_cloud_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestPropertyToolsRegistration:
    """Tests for property tools registration."""

    def test_registers_without_error(self):
        """Should register property tools without error."""
        from src.mcp_tools.properties import register_property_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_property_tools(mcp, resolve, logger)

        logger.info.assert_called()


class TestTimelineItemToolsRegistration:
    """Tests for timeline item tools registration."""

    def test_registers_without_error(self):
        """Should register timeline item tools without error."""
        from src.mcp_tools.timeline_items import register_timeline_item_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_timeline_item_tools(mcp, resolve, logger)

        logger.info.assert_called()
