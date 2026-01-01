#!/usr/bin/env python3
"""
DaVinci Resolve MCP Core Tools
Version info and page navigation
"""


def register_core_tools(mcp, resolve, logger):
    """Register core MCP tools and resources."""

    @mcp.resource("resolve://version")
    def get_resolve_version() -> str:
        """Get DaVinci Resolve version information."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"
        return f"{resolve.GetProductName()} {resolve.GetVersionString()}"

    @mcp.resource("resolve://current-page")
    def get_current_page() -> str:
        """Get the current page open in DaVinci Resolve."""
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"
        return resolve.GetCurrentPage()

    @mcp.tool()
    def switch_page(page: str) -> str:
        """Switch to a specific page in DaVinci Resolve.

        Args:
            page: The page to switch to. Options: 'media', 'cut', 'edit', 'fusion', 'color', 'fairlight', 'deliver'
        """
        if resolve is None:
            return "Error: Not connected to DaVinci Resolve"

        valid_pages = [
            "media",
            "cut",
            "edit",
            "fusion",
            "color",
            "fairlight",
            "deliver",
        ]
        page_lower = page.lower()

        if page_lower not in valid_pages:
            return f"Error: Invalid page name. Must be one of: {', '.join(valid_pages)}"

        result = resolve.OpenPage(page_lower)
        if result:
            return f"Successfully switched to {page_lower} page"
        else:
            return f"Failed to switch to {page_lower} page"

    logger.info("Registered core tools")
