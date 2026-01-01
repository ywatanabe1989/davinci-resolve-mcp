"""Tests for keyboard mark operations module."""

from unittest.mock import patch


class TestMarkSetIn:
    """Tests for mark_set_in function."""

    def test_sends_i_key(self):
        """Should send I for set mark in."""
        from src.utils.keyboard.marks import mark_set_in

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_set_in()
            mock_send.assert_called_once_with("i", "Set Mark In (I)")


class TestMarkSetOut:
    """Tests for mark_set_out function."""

    def test_sends_o_key(self):
        """Should send O for set mark out."""
        from src.utils.keyboard.marks import mark_set_out

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_set_out()
            mock_send.assert_called_once_with("o", "Set Mark Out (O)")


class TestMarkClip:
    """Tests for mark_clip function."""

    def test_sends_x_key(self):
        """Should send X for mark clip."""
        from src.utils.keyboard.marks import mark_clip

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_clip()
            mock_send.assert_called_once_with("x", "Mark Clip (X)")


class TestMarkGoToIn:
    """Tests for mark_go_to_in function."""

    def test_sends_shift_i(self):
        """Should send Shift+I for go to mark in."""
        from src.utils.keyboard.marks import mark_go_to_in

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_go_to_in()
            mock_send.assert_called_once_with("+i", "Go to Mark In (Shift+I)")


class TestMarkGoToOut:
    """Tests for mark_go_to_out function."""

    def test_sends_shift_o(self):
        """Should send Shift+O for go to mark out."""
        from src.utils.keyboard.marks import mark_go_to_out

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_go_to_out()
            mock_send.assert_called_once_with("+o", "Go to Mark Out (Shift+O)")


class TestMarkClearIn:
    """Tests for mark_clear_in function."""

    def test_sends_alt_i(self):
        """Should send Alt+I for clear mark in."""
        from src.utils.keyboard.marks import mark_clear_in

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_clear_in()
            mock_send.assert_called_once_with("%i", "Clear Mark In (Alt+I)")


class TestMarkClearOut:
    """Tests for mark_clear_out function."""

    def test_sends_alt_o(self):
        """Should send Alt+O for clear mark out."""
        from src.utils.keyboard.marks import mark_clear_out

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_clear_out()
            mock_send.assert_called_once_with("%o", "Clear Mark Out (Alt+O)")


class TestMarkClearBoth:
    """Tests for mark_clear_both function."""

    def test_sends_alt_x(self):
        """Should send Alt+X for clear both marks."""
        from src.utils.keyboard.marks import mark_clear_both

        with patch("src.utils.keyboard.marks.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mark_clear_both()
            mock_send.assert_called_once_with("%x", "Clear Mark In/Out (Alt+X)")
