#!/usr/bin/env python3
"""Color page node operation functions for DaVinci Resolve."""

from typing import Dict, Any
from .core import send_key_to_resolve


def node_add_serial() -> Dict[str, Any]:
    """Add serial node (Alt+S)."""
    return send_key_to_resolve("%s", "Add Serial Node (Alt+S)")


def node_add_parallel() -> Dict[str, Any]:
    """Add parallel node (Alt+P)."""
    return send_key_to_resolve("%p", "Add Parallel Node (Alt+P)")


def node_add_layer() -> Dict[str, Any]:
    """Add layer node (Alt+L)."""
    return send_key_to_resolve("%l", "Add Layer Node (Alt+L)")


def node_add_serial_before() -> Dict[str, Any]:
    """Add serial node before current (Alt+Q)."""
    return send_key_to_resolve("%q", "Add Serial Node Before (Alt+Q)")


def node_add_outside() -> Dict[str, Any]:
    """Add outside node (Alt+O in Color page)."""
    return send_key_to_resolve("%c", "Add Outside Node (Alt+C)")


def node_add_splitter_combiner() -> Dict[str, Any]:
    """Add splitter combiner node (Alt+Y)."""
    return send_key_to_resolve("%y", "Add Splitter Combiner (Alt+Y)")


def node_disable_current() -> Dict[str, Any]:
    """Disable/Enable current node (Ctrl+D)."""
    return send_key_to_resolve("^d", "Disable Current Node (Ctrl+D)")


def node_disable_all() -> Dict[str, Any]:
    """Disable/Enable all nodes (Alt+D)."""
    return send_key_to_resolve("%d", "Disable All Nodes (Alt+D)")


def node_bypass_grades() -> Dict[str, Any]:
    """Bypass all grades (Shift+D)."""
    return send_key_to_resolve("+d", "Bypass All Grades (Shift+D)")


def node_reset_grades() -> Dict[str, Any]:
    """Reset all grades and notes (Ctrl+Home)."""
    return send_key_to_resolve("^{HOME}", "Reset Grades/Notes (Ctrl+Home)")


def node_previous() -> Dict[str, Any]:
    """Go to previous node (Shift+Alt+;)."""
    return send_key_to_resolve("+%;", "Previous Node (Shift+Alt+;)")


def node_next() -> Dict[str, Any]:
    """Go to next node (Shift+Alt+')."""
    return send_key_to_resolve("+%'", "Next Node (Shift+Alt+')")


def node_extract_current() -> Dict[str, Any]:
    """Extract current node (E)."""
    return send_key_to_resolve("e", "Extract Node (E)")
