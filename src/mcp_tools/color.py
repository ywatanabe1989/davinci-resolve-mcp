#!/usr/bin/env python3
"""
DaVinci Resolve MCP Color Tools
Color page operations
"""

from typing import Dict, Any


def register_color_tools(mcp, resolve, logger):
    """Register color page MCP tools and resources."""

    @mcp.resource("resolve://color/current-node")
    def get_current_color_node() -> Dict[str, Any]:
        """Get information about the current node in the color page."""
        from src.api.color_operations import get_current_node as get_node_func

        return get_node_func(resolve)

    @mcp.resource("resolve://color/wheels/{node_index}")
    def get_color_wheel_params(node_index: int = None) -> Dict[str, Any]:
        """Get color wheel parameters for a specific node."""
        from src.api.color_operations import get_color_wheels as get_wheels_func

        return get_wheels_func(resolve, node_index)

    @mcp.tool()
    def apply_lut(lut_path: str, node_index: int = None) -> str:
        """Apply a LUT to a node in the color page."""
        from src.api.color_operations import apply_lut as apply_lut_func

        return apply_lut_func(resolve, lut_path, node_index)

    @mcp.tool()
    def set_color_wheel_param(
        wheel: str, param: str, value: float, node_index: int = None
    ) -> str:
        """Set a color wheel parameter for a node."""
        from src.api.color_operations import set_color_wheel_param as set_param_func

        return set_param_func(resolve, wheel, param, value, node_index)

    @mcp.tool()
    def add_node(node_type: str = "serial", label: str = None) -> str:
        """Add a new node to the current grade in the color page."""
        from src.api.color_operations import add_node as add_node_func

        return add_node_func(resolve, node_type, label)

    @mcp.tool()
    def copy_grade(
        source_clip_name: str = None, target_clip_name: str = None, mode: str = "full"
    ) -> str:
        """Copy a grade from one clip to another in the color page."""
        from src.api.color_operations import copy_grade as copy_grade_func

        return copy_grade_func(resolve, source_clip_name, target_clip_name, mode)

    logger.info("Registered color tools")
