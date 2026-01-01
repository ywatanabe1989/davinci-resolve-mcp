"""Tests for keyboard playback control module."""

from unittest.mock import patch


class TestPlaybackPlayPause:
    """Tests for playback_play_pause function."""

    def test_sends_space_key(self):
        """Should send space key for play/pause."""
        from src.utils.keyboard.playback import playback_play_pause

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_play_pause()
            mock_send.assert_called_once_with(" ", "Play/Pause (Space)")


class TestPlaybackStop:
    """Tests for playback_stop function."""

    def test_sends_k_key(self):
        """Should send K key for stop."""
        from src.utils.keyboard.playback import playback_stop

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_stop()
            mock_send.assert_called_once_with("k", "Stop (K)")


class TestPlaybackForward:
    """Tests for playback_forward function."""

    def test_sends_l_key(self):
        """Should send L key for play forward."""
        from src.utils.keyboard.playback import playback_forward

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_forward()
            mock_send.assert_called_once_with("l", "Play Forward (L)")


class TestPlaybackReverse:
    """Tests for playback_reverse function."""

    def test_sends_j_key(self):
        """Should send J key for play reverse."""
        from src.utils.keyboard.playback import playback_reverse

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_reverse()
            mock_send.assert_called_once_with("j", "Play Reverse (J)")


class TestPlaybackStepForward:
    """Tests for playback_step_forward function."""

    def test_sends_right_arrow(self):
        """Should send right arrow for step forward."""
        from src.utils.keyboard.playback import playback_step_forward

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_step_forward()
            mock_send.assert_called_once_with("{RIGHT}", "Step Forward (Right Arrow)")


class TestPlaybackStepBackward:
    """Tests for playback_step_backward function."""

    def test_sends_left_arrow(self):
        """Should send left arrow for step backward."""
        from src.utils.keyboard.playback import playback_step_backward

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_step_backward()
            mock_send.assert_called_once_with("{LEFT}", "Step Backward (Left Arrow)")


class TestPlaybackGoToStart:
    """Tests for playback_go_to_start function."""

    def test_sends_home_key(self):
        """Should send Home key for go to start."""
        from src.utils.keyboard.playback import playback_go_to_start

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_go_to_start()
            mock_send.assert_called_once_with("{HOME}", "Go to Start (Home)")


class TestPlaybackGoToEnd:
    """Tests for playback_go_to_end function."""

    def test_sends_end_key(self):
        """Should send End key for go to end."""
        from src.utils.keyboard.playback import playback_go_to_end

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_go_to_end()
            mock_send.assert_called_once_with("{END}", "Go to End (End)")


class TestPlaybackLoopToggle:
    """Tests for playback_loop_toggle function."""

    def test_sends_ctrl_slash(self):
        """Should send Ctrl+/ for loop toggle."""
        from src.utils.keyboard.playback import playback_loop_toggle

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_loop_toggle()
            mock_send.assert_called_once_with("^/", "Toggle Loop (Ctrl+/)")


class TestPlaybackFastForward:
    """Tests for playback_fast_forward function."""

    def test_sends_shift_l(self):
        """Should send Shift+L for fast forward."""
        from src.utils.keyboard.playback import playback_fast_forward

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_fast_forward()
            mock_send.assert_called_once_with("+l", "Fast Forward (Shift+L)")


class TestPlaybackFastReverse:
    """Tests for playback_fast_reverse function."""

    def test_sends_shift_j(self):
        """Should send Shift+J for fast reverse."""
        from src.utils.keyboard.playback import playback_fast_reverse

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_fast_reverse()
            mock_send.assert_called_once_with("+j", "Fast Reverse (Shift+J)")


class TestPlaybackPlayAround:
    """Tests for playback_play_around function."""

    def test_sends_slash(self):
        """Should send / for play around."""
        from src.utils.keyboard.playback import playback_play_around

        with patch("src.utils.keyboard.playback.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            playback_play_around()
            mock_send.assert_called_once_with("/", "Play Around (/)")
