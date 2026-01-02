"""Tests for keyboard node operations module."""

from unittest.mock import patch


class TestNodeAddSerial:
    """Tests for node_add_serial function."""

    def test_sends_alt_s(self):
        """Should send Alt+S for add serial node."""
        from src.utils.keyboard.nodes import node_add_serial

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_add_serial()
            mock_send.assert_called_once_with("%s", "Add Serial Node (Alt+S)")


class TestNodeAddParallel:
    """Tests for node_add_parallel function."""

    def test_sends_alt_p(self):
        """Should send Alt+P for add parallel node."""
        from src.utils.keyboard.nodes import node_add_parallel

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_add_parallel()
            mock_send.assert_called_once_with("%p", "Add Parallel Node (Alt+P)")


class TestNodeAddLayer:
    """Tests for node_add_layer function."""

    def test_sends_alt_l(self):
        """Should send Alt+L for add layer node."""
        from src.utils.keyboard.nodes import node_add_layer

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_add_layer()
            mock_send.assert_called_once_with("%l", "Add Layer Node (Alt+L)")


class TestNodeDisableCurrent:
    """Tests for node_disable_current function."""

    def test_sends_ctrl_d(self):
        """Should send Ctrl+D for disable current node."""
        from src.utils.keyboard.nodes import node_disable_current

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_disable_current()
            mock_send.assert_called_once_with("^d", "Disable Current Node (Ctrl+D)")


class TestNodeDisableAll:
    """Tests for node_disable_all function."""

    def test_sends_alt_d(self):
        """Should send Alt+D for disable all nodes."""
        from src.utils.keyboard.nodes import node_disable_all

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_disable_all()
            mock_send.assert_called_once_with("%d", "Disable All Nodes (Alt+D)")


class TestNodeBypassGrades:
    """Tests for node_bypass_grades function."""

    def test_sends_shift_d(self):
        """Should send Shift+D for bypass grades."""
        from src.utils.keyboard.nodes import node_bypass_grades

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_bypass_grades()
            mock_send.assert_called_once_with("+d", "Bypass All Grades (Shift+D)")


class TestNodeResetGrades:
    """Tests for node_reset_grades function."""

    def test_sends_ctrl_home(self):
        """Should send Ctrl+Home for reset grades."""
        from src.utils.keyboard.nodes import node_reset_grades

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_reset_grades()
            mock_send.assert_called_once_with(
                "^{HOME}", "Reset Grades/Notes (Ctrl+Home)"
            )


class TestNodeExtractCurrent:
    """Tests for node_extract_current function."""

    def test_sends_e_key(self):
        """Should send E for extract current node."""
        from src.utils.keyboard.nodes import node_extract_current

        with patch("src.utils.keyboard.nodes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            node_extract_current()
            mock_send.assert_called_once_with("e", "Extract Node (E)")
