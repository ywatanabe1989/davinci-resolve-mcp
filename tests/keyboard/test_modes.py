"""Tests for keyboard edit mode module."""

from unittest.mock import patch


class TestModeSelection:
    """Tests for mode_selection function."""

    def test_sends_a_key(self):
        """Should send A for selection mode."""
        from src.utils.keyboard.modes import mode_selection

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_selection()
            mock_send.assert_called_once_with("a", "Selection Mode (A)")


class TestModeBlade:
    """Tests for mode_blade function."""

    def test_sends_b_key(self):
        """Should send B for blade mode."""
        from src.utils.keyboard.modes import mode_blade

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_blade()
            mock_send.assert_called_once_with("b", "Blade Mode (B)")


class TestModeTrim:
    """Tests for mode_trim function."""

    def test_sends_t_key(self):
        """Should send T for trim mode."""
        from src.utils.keyboard.modes import mode_trim

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_trim()
            mock_send.assert_called_once_with("t", "Trim Mode (T)")


class TestModeDynamicTrim:
    """Tests for mode_dynamic_trim function."""

    def test_sends_w_key(self):
        """Should send W for dynamic trim mode."""
        from src.utils.keyboard.modes import mode_dynamic_trim

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_dynamic_trim()
            mock_send.assert_called_once_with("w", "Dynamic Trim Mode (W)")


class TestModeSlipSlide:
    """Tests for mode_slip_slide function."""

    def test_sends_s_key(self):
        """Should send S for slip/slide mode."""
        from src.utils.keyboard.modes import mode_slip_slide

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_slip_slide()
            mock_send.assert_called_once_with("s", "Slip/Slide Mode (S)")


class TestModeHandTool:
    """Tests for mode_hand_tool function."""

    def test_sends_h_key(self):
        """Should send H for hand tool."""
        from src.utils.keyboard.modes import mode_hand_tool

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            mode_hand_tool()
            mock_send.assert_called_once_with("h", "Hand Tool (H)")


class TestToggleSnapping:
    """Tests for toggle_snapping function."""

    def test_sends_n_key(self):
        """Should send N for toggle snapping."""
        from src.utils.keyboard.modes import toggle_snapping

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            toggle_snapping()
            mock_send.assert_called_once_with("n", "Toggle Snapping (N)")


class TestToggleAudioScrubbing:
    """Tests for toggle_audio_scrubbing function."""

    def test_sends_shift_s(self):
        """Should send Shift+S for audio scrubbing."""
        from src.utils.keyboard.modes import toggle_audio_scrubbing

        with patch("src.utils.keyboard.modes.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            toggle_audio_scrubbing()
            mock_send.assert_called_once_with("+s", "Audio Scrubbing (Shift+S)")
