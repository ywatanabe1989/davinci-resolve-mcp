"""Tests for keyboard color page module."""

from unittest.mock import patch


class TestColorGrabStill:
    """Tests for color_grab_still function."""

    def test_sends_ctrl_alt_g(self):
        """Should send Ctrl+Alt+G for grab still."""
        from src.utils.keyboard.color import color_grab_still

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_grab_still()
            mock_send.assert_called_once_with("^%g", "Grab Still (Ctrl+Alt+G)")


class TestColorAutoBalance:
    """Tests for color_auto_balance function."""

    def test_sends_alt_a(self):
        """Should send Alt+A for auto color balance."""
        from src.utils.keyboard.color import color_auto_balance

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_auto_balance()
            mock_send.assert_called_once_with("%a", "Auto Color (Alt+A)")


class TestColorHighlight:
    """Tests for color_highlight function."""

    def test_sends_shift_h(self):
        """Should send Shift+H for toggle highlight."""
        from src.utils.keyboard.color import color_highlight

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_highlight()
            mock_send.assert_called_once_with("+h", "Toggle Highlight (Shift+H)")


class TestColorAddVersion:
    """Tests for color_add_version function."""

    def test_sends_ctrl_y(self):
        """Should send Ctrl+Y for add version."""
        from src.utils.keyboard.color import color_add_version

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_add_version()
            mock_send.assert_called_once_with("^y", "Add Version (Ctrl+Y)")


class TestColorLoadMemoryA:
    """Tests for color_load_memory_a function."""

    def test_sends_ctrl_1(self):
        """Should send Ctrl+1 for load memory A."""
        from src.utils.keyboard.color import color_load_memory_a

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_load_memory_a()
            mock_send.assert_called_once_with("^1", "Load Memory A (Ctrl+1)")


class TestColorSaveMemoryA:
    """Tests for color_save_memory_a function."""

    def test_sends_alt_1(self):
        """Should send Alt+1 for save memory A."""
        from src.utils.keyboard.color import color_save_memory_a

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_save_memory_a()
            mock_send.assert_called_once_with("%1", "Save Memory A (Alt+1)")


class TestColorLoadMemoryB:
    """Tests for color_load_memory_b function."""

    def test_sends_ctrl_2(self):
        """Should send Ctrl+2 for load memory B."""
        from src.utils.keyboard.color import color_load_memory_b

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_load_memory_b()
            mock_send.assert_called_once_with("^2", "Load Memory B (Ctrl+2)")


class TestColorSaveMemoryB:
    """Tests for color_save_memory_b function."""

    def test_sends_alt_2(self):
        """Should send Alt+2 for save memory B."""
        from src.utils.keyboard.color import color_save_memory_b

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_save_memory_b()
            mock_send.assert_called_once_with("%2", "Save Memory B (Alt+2)")


class TestColorLoadMemoryC:
    """Tests for color_load_memory_c function."""

    def test_sends_ctrl_3(self):
        """Should send Ctrl+3 for load memory C."""
        from src.utils.keyboard.color import color_load_memory_c

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_load_memory_c()
            mock_send.assert_called_once_with("^3", "Load Memory C (Ctrl+3)")


class TestColorSaveMemoryC:
    """Tests for color_save_memory_c function."""

    def test_sends_alt_3(self):
        """Should send Alt+3 for save memory C."""
        from src.utils.keyboard.color import color_save_memory_c

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_save_memory_c()
            mock_send.assert_called_once_with("%3", "Save Memory C (Alt+3)")


class TestColorLoadMemoryD:
    """Tests for color_load_memory_d function."""

    def test_sends_ctrl_4(self):
        """Should send Ctrl+4 for load memory D."""
        from src.utils.keyboard.color import color_load_memory_d

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_load_memory_d()
            mock_send.assert_called_once_with("^4", "Load Memory D (Ctrl+4)")


class TestColorSaveMemoryD:
    """Tests for color_save_memory_d function."""

    def test_sends_alt_4(self):
        """Should send Alt+4 for save memory D."""
        from src.utils.keyboard.color import color_save_memory_d

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_save_memory_d()
            mock_send.assert_called_once_with("%4", "Save Memory D (Alt+4)")


class TestColorApplyGradeFromOnePrior:
    """Tests for color_apply_grade_from_one_prior function."""

    def test_sends_equals(self):
        """Should send = for apply grade from one prior."""
        from src.utils.keyboard.color import color_apply_grade_from_one_prior

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_apply_grade_from_one_prior()
            mock_send.assert_called_once_with("=", "Apply Grade One Prior (=)")


class TestColorApplyGradeFromTwoPrior:
    """Tests for color_apply_grade_from_two_prior function."""

    def test_sends_minus(self):
        """Should send - for apply grade from two prior."""
        from src.utils.keyboard.color import color_apply_grade_from_two_prior

        with patch("src.utils.keyboard.color.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            color_apply_grade_from_two_prior()
            mock_send.assert_called_once_with("-", "Apply Grade Two Prior (-)")
