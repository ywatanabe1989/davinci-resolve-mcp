"""Tests for keyboard timeline navigation module."""

from unittest.mock import patch


class TestTimelinePreviousClip:
    """Tests for timeline_previous_clip function."""

    def test_sends_up_arrow(self):
        """Should send Up Arrow for previous clip."""
        from src.utils.keyboard.timeline import timeline_previous_clip

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_previous_clip()
            mock_send.assert_called_once_with("{UP}", "Previous Clip (Up Arrow)")


class TestTimelineNextClip:
    """Tests for timeline_next_clip function."""

    def test_sends_down_arrow(self):
        """Should send Down Arrow for next clip."""
        from src.utils.keyboard.timeline import timeline_next_clip

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_next_clip()
            mock_send.assert_called_once_with("{DOWN}", "Next Clip (Down Arrow)")


class TestTimelineStep1SecondForward:
    """Tests for timeline_step_1_second_forward function."""

    def test_sends_shift_right(self):
        """Should send Shift+Right for step 1 second forward."""
        from src.utils.keyboard.timeline import timeline_step_1_second_forward

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_step_1_second_forward()
            mock_send.assert_called_once_with(
                "+{RIGHT}", "Step 1 Second Forward (Shift+Right)"
            )


class TestTimelineStep1SecondBackward:
    """Tests for timeline_step_1_second_backward function."""

    def test_sends_shift_left(self):
        """Should send Shift+Left for step 1 second backward."""
        from src.utils.keyboard.timeline import timeline_step_1_second_backward

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_step_1_second_backward()
            mock_send.assert_called_once_with(
                "+{LEFT}", "Step 1 Second Backward (Shift+Left)"
            )


class TestTimelineGoToFirstFrame:
    """Tests for timeline_go_to_first_frame function."""

    def test_sends_semicolon(self):
        """Should send ; for go to first frame."""
        from src.utils.keyboard.timeline import timeline_go_to_first_frame

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_go_to_first_frame()
            mock_send.assert_called_once_with(";", "First Frame (;)")


class TestTimelineGoToLastFrame:
    """Tests for timeline_go_to_last_frame function."""

    def test_sends_apostrophe(self):
        """Should send ' for go to last frame."""
        from src.utils.keyboard.timeline import timeline_go_to_last_frame

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_go_to_last_frame()
            mock_send.assert_called_once_with("'", "Last Frame (')")


class TestTimelineGoToPrevKeyframe:
    """Tests for timeline_go_to_prev_keyframe function."""

    def test_sends_left_bracket(self):
        """Should send [ for previous keyframe."""
        from src.utils.keyboard.timeline import timeline_go_to_prev_keyframe

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_go_to_prev_keyframe()
            mock_send.assert_called_once_with("[", "Previous Keyframe ([)")


class TestTimelineGoToNextKeyframe:
    """Tests for timeline_go_to_next_keyframe function."""

    def test_sends_right_bracket(self):
        """Should send ] for next keyframe."""
        from src.utils.keyboard.timeline import timeline_go_to_next_keyframe

        with patch("src.utils.keyboard.timeline.send_key_to_resolve") as mock_send:
            mock_send.return_value = {"success": True, "message": "OK"}
            timeline_go_to_next_keyframe()
            mock_send.assert_called_once_with("]", "Next Keyframe (])")
