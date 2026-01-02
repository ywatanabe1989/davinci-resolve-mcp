"""Tests for MCP tools registration functions."""

import pytest
from unittest.mock import Mock, MagicMock


# Parametrized test for all module imports
TOOL_MODULES = [
    ("src.mcp_tools", "register_all_tools"),
    ("src.mcp_tools.core", "register_core_tools"),
    ("src.mcp_tools.project", "register_project_tools"),
    ("src.mcp_tools.timeline", "register_timeline_tools"),
    ("src.mcp_tools.media", "register_media_tools"),
    ("src.mcp_tools.color", "register_color_tools"),
    ("src.mcp_tools.delivery", "register_delivery_tools"),
    ("src.mcp_tools.cache", "register_cache_tools"),
    ("src.mcp_tools.keyframes", "register_keyframe_tools"),
    ("src.mcp_tools.presets", "register_preset_tools"),
    ("src.mcp_tools.inspection", "register_inspection_tools"),
    ("src.mcp_tools.layout", "register_layout_tools"),
    ("src.mcp_tools.app", "register_app_tools"),
    ("src.mcp_tools.cloud", "register_cloud_tools"),
    ("src.mcp_tools.properties", "register_property_tools"),
    ("src.mcp_tools.timeline_items", "register_timeline_item_tools"),
]


class TestModuleImports:
    """Tests that all MCP tool modules can be imported."""

    @pytest.mark.parametrize("module_path,func_name", TOOL_MODULES)
    def test_module_imports_and_is_callable(self, module_path, func_name):
        """Should import module and verify function is callable."""
        import importlib

        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        assert callable(func)


class TestRegisterAllTools:
    """Tests for register_all_tools function."""

    def test_registers_all_tool_modules(self):
        """Should call all registration functions."""
        from src.mcp_tools import register_all_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_all_tools(mcp, resolve, logger)

        # Should log for each module (15 modules)
        assert logger.info.call_count >= 15

    def test_mcp_decorators_are_called(self):
        """Should use mcp.tool and mcp.resource decorators."""
        from src.mcp_tools import register_all_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_all_tools(mcp, resolve, logger)

        # Verify decorators were called
        assert mcp.tool.called or mcp.resource.called


class TestCoreTools:
    """Tests for core tools functionality."""

    def test_switch_page_rejects_invalid_page(self):
        """Should return error for invalid page name."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        # Capture the registered tool
        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_core_tools(mcp, resolve, logger)

        # Call the switch_page tool with invalid page
        result = registered_tools["switch_page"]("invalid_page")
        assert "Error" in result
        assert "Invalid page name" in result

    def test_switch_page_accepts_valid_pages(self):
        """Should accept all valid page names."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = Mock()
        resolve.OpenPage.return_value = True
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_core_tools(mcp, resolve, logger)

        valid_pages = [
            "media",
            "cut",
            "edit",
            "fusion",
            "color",
            "fairlight",
            "deliver",
        ]
        for page in valid_pages:
            result = registered_tools["switch_page"](page)
            assert "Successfully" in result or "switched" in result.lower()

    def test_switch_page_returns_error_when_not_connected(self):
        """Should return error when resolve is None."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = None
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_core_tools(mcp, resolve, logger)

        result = registered_tools["switch_page"]("edit")
        assert "Error" in result
        assert "Not connected" in result


class TestCoreResources:
    """Tests for core resource functionality."""

    def test_get_version_returns_error_when_not_connected(self):
        """Should return error when resolve is None."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = None
        logger = Mock()

        registered_resources = {}

        def capture_resource(uri):
            def decorator(func):
                registered_resources[uri] = func
                return func

            return decorator

        mcp.resource = capture_resource

        register_core_tools(mcp, resolve, logger)

        result = registered_resources["resolve://version"]()
        assert "Error" in result
        assert "Not connected" in result

    def test_get_version_returns_product_info(self):
        """Should return product name and version."""
        from src.mcp_tools.core import register_core_tools

        mcp = MagicMock()
        resolve = Mock()
        resolve.GetProductName.return_value = "DaVinci Resolve"
        resolve.GetVersionString.return_value = "18.5.1"
        logger = Mock()

        registered_resources = {}

        def capture_resource(uri):
            def decorator(func):
                registered_resources[uri] = func
                return func

            return decorator

        mcp.resource = capture_resource

        register_core_tools(mcp, resolve, logger)

        result = registered_resources["resolve://version"]()
        assert "DaVinci Resolve" in result
        assert "18.5.1" in result


class TestProjectTools:
    """Tests for project tools functionality."""

    def test_open_project_rejects_empty_name(self):
        """Should return error for empty project name."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_project_tools(mcp, resolve, logger)

        result = registered_tools["open_project"]("")
        assert "Error" in result
        assert "empty" in result.lower()

    def test_open_project_rejects_nonexistent_project(self):
        """Should return error when project doesn't exist."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        project_manager = Mock()
        project_manager.GetProjectListInCurrentFolder.return_value = [
            "Project1",
            "Project2",
        ]
        resolve.GetProjectManager.return_value = project_manager
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_project_tools(mcp, resolve, logger)

        result = registered_tools["open_project"]("NonExistent")
        assert "Error" in result
        assert "not found" in result.lower()
        assert "Project1" in result  # Should list available projects

    def test_create_project_rejects_duplicate_name(self):
        """Should return error when project already exists."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        project_manager = Mock()
        project_manager.GetProjectListInCurrentFolder.return_value = ["ExistingProject"]
        resolve.GetProjectManager.return_value = project_manager
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_project_tools(mcp, resolve, logger)

        result = registered_tools["create_project"]("ExistingProject")
        assert "Error" in result
        assert "already exists" in result

    def test_save_project_returns_error_when_no_project_open(self):
        """Should return error when no project is open."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        project_manager = Mock()
        project_manager.GetCurrentProject.return_value = None
        resolve.GetProjectManager.return_value = project_manager
        logger = Mock()

        registered_tools = {}

        def capture_tool():
            def decorator(func):
                registered_tools[func.__name__] = func
                return func

            return decorator

        mcp.tool = capture_tool

        register_project_tools(mcp, resolve, logger)

        result = registered_tools["save_project"]()
        assert "Error" in result
        assert "No project" in result


class TestProjectResources:
    """Tests for project resource functionality."""

    def test_list_projects_returns_project_list(self):
        """Should return list of projects."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        project_manager = Mock()
        project_manager.GetProjectListInCurrentFolder.return_value = [
            "Project1",
            "Project2",
            "Project3",
        ]
        resolve.GetProjectManager.return_value = project_manager
        logger = Mock()

        registered_resources = {}

        def capture_resource(uri):
            def decorator(func):
                registered_resources[uri] = func
                return func

            return decorator

        mcp.resource = capture_resource

        register_project_tools(mcp, resolve, logger)

        result = registered_resources["resolve://projects"]()
        assert isinstance(result, list)
        assert len(result) == 3
        assert "Project1" in result

    def test_get_current_project_returns_name(self):
        """Should return current project name."""
        from src.mcp_tools.project import register_project_tools

        mcp = MagicMock()
        resolve = Mock()
        project_manager = Mock()
        current_project = Mock()
        current_project.GetName.return_value = "MyProject"
        project_manager.GetCurrentProject.return_value = current_project
        resolve.GetProjectManager.return_value = project_manager
        logger = Mock()

        registered_resources = {}

        def capture_resource(uri):
            def decorator(func):
                registered_resources[uri] = func
                return func

            return decorator

        mcp.resource = capture_resource

        register_project_tools(mcp, resolve, logger)

        result = registered_resources["resolve://current-project"]()
        assert result == "MyProject"


class TestToolRegistrationModules:
    """Parametrized tests for all tool registration modules."""

    @pytest.mark.parametrize(
        "module_path,func_name",
        [
            ("src.mcp_tools.core", "register_core_tools"),
            ("src.mcp_tools.project", "register_project_tools"),
            ("src.mcp_tools.timeline", "register_timeline_tools"),
            ("src.mcp_tools.media", "register_media_tools"),
            ("src.mcp_tools.color", "register_color_tools"),
            ("src.mcp_tools.delivery", "register_delivery_tools"),
            ("src.mcp_tools.cache", "register_cache_tools"),
            ("src.mcp_tools.keyframes", "register_keyframe_tools"),
            ("src.mcp_tools.presets", "register_preset_tools"),
            ("src.mcp_tools.inspection", "register_inspection_tools"),
            ("src.mcp_tools.layout", "register_layout_tools"),
            ("src.mcp_tools.app", "register_app_tools"),
            ("src.mcp_tools.cloud", "register_cloud_tools"),
            ("src.mcp_tools.properties", "register_property_tools"),
            ("src.mcp_tools.timeline_items", "register_timeline_item_tools"),
        ],
    )
    def test_registration_does_not_raise(self, module_path, func_name):
        """Should register without raising exceptions."""
        import importlib

        module = importlib.import_module(module_path)
        register_func = getattr(module, func_name)

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        # Should not raise
        register_func(mcp, resolve, logger)

    @pytest.mark.parametrize(
        "module_path,func_name",
        [
            ("src.mcp_tools.core", "register_core_tools"),
            ("src.mcp_tools.project", "register_project_tools"),
            ("src.mcp_tools.timeline", "register_timeline_tools"),
            ("src.mcp_tools.media", "register_media_tools"),
            ("src.mcp_tools.color", "register_color_tools"),
            ("src.mcp_tools.delivery", "register_delivery_tools"),
            ("src.mcp_tools.cache", "register_cache_tools"),
            ("src.mcp_tools.keyframes", "register_keyframe_tools"),
            ("src.mcp_tools.presets", "register_preset_tools"),
            ("src.mcp_tools.inspection", "register_inspection_tools"),
            ("src.mcp_tools.layout", "register_layout_tools"),
            ("src.mcp_tools.app", "register_app_tools"),
            ("src.mcp_tools.cloud", "register_cloud_tools"),
            ("src.mcp_tools.properties", "register_property_tools"),
            ("src.mcp_tools.timeline_items", "register_timeline_item_tools"),
        ],
    )
    def test_registration_logs_info(self, module_path, func_name):
        """Should log info message after registration."""
        import importlib

        module = importlib.import_module(module_path)
        register_func = getattr(module, func_name)

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_func(mcp, resolve, logger)

        # Should log at least one info message
        assert logger.info.called

    @pytest.mark.parametrize(
        "module_path,func_name",
        [
            ("src.mcp_tools.core", "register_core_tools"),
            ("src.mcp_tools.project", "register_project_tools"),
            ("src.mcp_tools.timeline", "register_timeline_tools"),
            ("src.mcp_tools.media", "register_media_tools"),
            ("src.mcp_tools.color", "register_color_tools"),
            ("src.mcp_tools.delivery", "register_delivery_tools"),
        ],
    )
    def test_registration_uses_mcp_decorators(self, module_path, func_name):
        """Should use mcp.tool or mcp.resource decorators."""
        import importlib

        module = importlib.import_module(module_path)
        register_func = getattr(module, func_name)

        mcp = MagicMock()
        resolve = Mock()
        logger = Mock()

        register_func(mcp, resolve, logger)

        # At least one decorator should be called
        assert mcp.tool.called or mcp.resource.called


class TestNullResolveHandling:
    """Tests that tools handle null resolve gracefully."""

    @pytest.mark.parametrize(
        "module_path,func_name",
        [
            ("src.mcp_tools.core", "register_core_tools"),
            ("src.mcp_tools.project", "register_project_tools"),
            ("src.mcp_tools.timeline", "register_timeline_tools"),
            ("src.mcp_tools.media", "register_media_tools"),
            ("src.mcp_tools.color", "register_color_tools"),
            ("src.mcp_tools.delivery", "register_delivery_tools"),
        ],
    )
    def test_registration_works_with_null_resolve(self, module_path, func_name):
        """Should register successfully even with null resolve."""
        import importlib

        module = importlib.import_module(module_path)
        register_func = getattr(module, func_name)

        mcp = MagicMock()
        resolve = None  # Null resolve
        logger = Mock()

        # Should not raise
        register_func(mcp, resolve, logger)
        assert logger.info.called
