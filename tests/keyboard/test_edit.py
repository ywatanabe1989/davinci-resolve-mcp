"""Tests for keyboard edit operations module."""

from unittest.mock import patch


class TestEditCutAtPlayhead:
    """Tests for edit_cut_at_playhead function."""

    def test_sends_ctrl_b(self):
        """Should send Ctrl+B for cut at playhead."""
        from src.utils.keyboard.edit import edit_cut_at_playhead

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_cut_at_playhead()
            mock_send.assert_called_once_with("^b", "Cut at Playhead (Ctrl+B)")


class TestEditRippleDelete:
    """Tests for edit_ripple_delete function."""

    def test_sends_delete(self):
        """Should send Delete for ripple delete."""
        from src.utils.keyboard.edit import edit_ripple_delete

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_ripple_delete()
            mock_send.assert_called_once_with("{DELETE}", "Ripple Delete (Delete)")


class TestEditDelete:
    """Tests for edit_delete function."""

    def test_sends_backspace(self):
        """Should send Backspace for delete."""
        from src.utils.keyboard.edit import edit_delete

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_delete()
            mock_send.assert_called_once_with("{BACKSPACE}", "Delete (Backspace)")


class TestEditUndo:
    """Tests for edit_undo function."""

    def test_sends_ctrl_z(self):
        """Should send Ctrl+Z for undo."""
        from src.utils.keyboard.edit import edit_undo

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_undo()
            mock_send.assert_called_once_with("^z", "Undo (Ctrl+Z)")


class TestEditRedo:
    """Tests for edit_redo function."""

    def test_sends_ctrl_shift_z(self):
        """Should send Ctrl+Shift+Z for redo."""
        from src.utils.keyboard.edit import edit_redo

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_redo()
            mock_send.assert_called_once_with("^+z", "Redo (Ctrl+Shift+Z)")


class TestEditTrimStart:
    """Tests for edit_trim_start function."""

    def test_sends_shift_bracket(self):
        """Should send Shift+[ for trim start."""
        from src.utils.keyboard.edit import edit_trim_start

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_trim_start()
            mock_send.assert_called_once_with("+[", "Trim Start (Shift+[)")


class TestEditTrimEnd:
    """Tests for edit_trim_end function."""

    def test_sends_shift_bracket(self):
        """Should send Shift+] for trim end."""
        from src.utils.keyboard.edit import edit_trim_end

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_trim_end()
            mock_send.assert_called_once_with("+]", "Trim End (Shift+])")


class TestEditInsert:
    """Tests for edit_insert function."""

    def test_sends_f9(self):
        """Should send F9 for insert."""
        from src.utils.keyboard.edit import edit_insert

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_insert()
            mock_send.assert_called_once_with("{F9}", "Insert (F9)")


class TestEditOverwrite:
    """Tests for edit_overwrite function."""

    def test_sends_f10(self):
        """Should send F10 for overwrite."""
        from src.utils.keyboard.edit import edit_overwrite

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_overwrite()
            mock_send.assert_called_once_with("{F10}", "Overwrite (F10)")


class TestEditCopy:
    """Tests for edit_copy function."""

    def test_sends_ctrl_c(self):
        """Should send Ctrl+C for copy."""
        from src.utils.keyboard.edit import edit_copy

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_copy()
            mock_send.assert_called_once_with("^c", "Copy (Ctrl+C)")


class TestEditCut:
    """Tests for edit_cut function."""

    def test_sends_ctrl_x(self):
        """Should send Ctrl+X for cut."""
        from src.utils.keyboard.edit import edit_cut

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_cut()
            mock_send.assert_called_once_with("^x", "Cut (Ctrl+X)")


class TestEditPaste:
    """Tests for edit_paste function."""

    def test_sends_ctrl_v(self):
        """Should send Ctrl+V for paste."""
        from src.utils.keyboard.edit import edit_paste

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_paste()
            mock_send.assert_called_once_with("^v", "Paste (Ctrl+V)")


class TestEditReplace:
    """Tests for edit_replace function."""

    def test_sends_f11(self):
        """Should send F11 for replace."""
        from src.utils.keyboard.edit import edit_replace

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_replace()
            mock_send.assert_called_once_with("{F11}", "Replace (F11)")


class TestEditPlaceOnTop:
    """Tests for edit_place_on_top function."""

    def test_sends_f12(self):
        """Should send F12 for place on top."""
        from src.utils.keyboard.edit import edit_place_on_top

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_place_on_top()
            mock_send.assert_called_once_with("{F12}", "Place on Top (F12)")


class TestEditAppendToEnd:
    """Tests for edit_append_to_end function."""

    def test_sends_shift_f12(self):
        """Should send Shift+F12 for append to end."""
        from src.utils.keyboard.edit import edit_append_to_end

        with patch("src.utils.keyboard.edit.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            edit_append_to_end()
            mock_send.assert_called_once_with("+{F12}", "Append to End (Shift+F12)")
