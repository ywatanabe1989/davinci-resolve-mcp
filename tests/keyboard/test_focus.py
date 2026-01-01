"""Tests for keyboard focus management module."""

from unittest.mock import Mock, patch


class TestSaveUserState:
    """Tests for save_user_state function."""

    def test_returns_error_on_unsupported_platform(self):
        """Should return error when platform is not Windows/WSL."""
        from src.utils.keyboard.focus import save_user_state

        with patch("src.utils.keyboard.focus.get_platform_type", return_value="linux"):
            result = save_user_state()
            assert result["success"] is False
            assert "not supported" in result["error"].lower()

    def test_saves_window_handle_and_cursor(self):
        """Should save window handle and cursor position."""
        from src.utils.keyboard.focus import save_user_state

        mock_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout=mock_output)
                result = save_user_state()

                assert result["success"] is True
                assert result["state"]["window_handle"] == "12345"
                assert result["state"]["window_title"] == "Emacs"
                assert result["state"]["cursor_x"] == 100
                assert result["state"]["cursor_y"] == 200

    def test_handles_exception(self):
        """Should handle exceptions gracefully."""
        from src.utils.keyboard.focus import save_user_state

        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = Exception("PowerShell failed")
                result = save_user_state()

                assert result["success"] is False
                assert "PowerShell failed" in result["error"]


class TestRestoreUserState:
    """Tests for restore_user_state function."""

    def test_returns_error_when_no_saved_state(self):
        """Should return error when no state has been saved."""
        from src.utils.keyboard.focus import restore_user_state, clear_saved_state

        clear_saved_state()
        result = restore_user_state()
        assert result["success"] is False
        assert "No saved state" in result["error"]

    def test_restores_saved_state(self):
        """Should restore previously saved state."""
        from src.utils.keyboard.focus import (
            save_user_state,
            restore_user_state,
        )

        mock_save_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout=mock_save_output)
                save_user_state()

                mock_run.return_value = Mock(stdout="RESTORED")
                result = restore_user_state()

                assert result["success"] is True
                assert "Emacs" in result["message"]
                assert "(100, 200)" in result["message"]

    def test_clears_state_after_restore(self):
        """Should clear saved state after successful restore."""
        from src.utils.keyboard.focus import (
            save_user_state,
            restore_user_state,
            get_saved_state,
        )

        mock_save_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout=mock_save_output)
                save_user_state()
                assert get_saved_state() is not None

                mock_run.return_value = Mock(stdout="RESTORED")
                restore_user_state()
                assert get_saved_state() is None


class TestResolveUIContext:
    """Tests for ResolveUIContext context manager."""

    def test_saves_and_restores_state(self):
        """Should save state on enter and restore on exit."""
        from src.utils.keyboard.focus import ResolveUIContext

        mock_save_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout=mock_save_output)

                with ResolveUIContext("Test operation"):
                    # Save should have been called
                    assert mock_run.call_count == 1

                    mock_run.return_value = Mock(stdout="RESTORED")

                # Restore should have been called on exit
                assert mock_run.call_count == 2

    def test_restores_even_on_exception(self):
        """Should restore state even if an exception occurs."""
        from src.utils.keyboard.focus import ResolveUIContext

        mock_save_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(stdout=mock_save_output)

                try:
                    with ResolveUIContext("Test operation"):
                        mock_run.return_value = Mock(stdout="RESTORED")
                        raise ValueError("Test error")
                except ValueError:
                    pass

                # Restore should still have been called
                assert mock_run.call_count == 2


class TestWithUserStatePreserved:
    """Tests for with_user_state_preserved decorator."""

    def test_wraps_function_with_save_restore(self):
        """Should save state before and restore after function execution."""
        from src.utils.keyboard.focus import with_user_state_preserved

        mock_save_output = "HANDLE:12345\nTITLE:Emacs\nCURSOR:100,200"
        call_order = []

        with patch("src.utils.keyboard.focus.get_platform_type", return_value="wsl"):
            with patch("subprocess.run") as mock_run:

                def side_effect(*args, **kwargs):
                    # Check the PowerShell script content (args[0][2])
                    script = args[0][2] if len(args[0]) > 2 else ""
                    if "GetCursorPos" in script:
                        call_order.append("save")
                        return Mock(stdout=mock_save_output)
                    else:
                        call_order.append("restore")
                        return Mock(stdout="RESTORED")

                mock_run.side_effect = side_effect

                @with_user_state_preserved
                def test_func():
                    call_order.append("function")
                    return "result"

                result = test_func()

                assert result == "result"
                assert call_order == ["save", "function", "restore"]
