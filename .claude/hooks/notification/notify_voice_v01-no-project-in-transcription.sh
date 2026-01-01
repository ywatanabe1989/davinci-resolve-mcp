#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-18 (ywatanabe)"
# File: ~/.claude/to_claude/hooks/notify_voice.sh
# Description: Voice notification when Claude needs attention (Notification hook)
#
# Notification types:
#   - idle_prompt: Claude is waiting for input
#   - permission_prompt: Claude needs permission
#
# Uses scitex-audio MCP server (gTTS backend at 1.5x speed)
# Fallback: say (macOS), espeak (Linux), or terminal bell

set -euo pipefail

# Read hook input JSON from stdin
INPUT=$(cat)

# Extract notification_type from hook input
NOTIFICATION_TYPE=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('notification_type', '') or '')
" 2>/dev/null || echo "")

# If no notification type, nothing to do
[ -n "$NOTIFICATION_TYPE" ] || exit 0

# Function to speak using scitex-audio MCP (via direct Python call)
speak_mcp() {
    local text="$1"
    # Try using the scitex-audio speak function directly
    python3 -c "
import sys
try:
    from scitex.audio import speak
    speak('$text', speed=1.5, backend='gtts', wait=False)
except ImportError:
    # Fallback: print to stderr and use terminal method
    sys.exit(1)
" 2>/dev/null && return 0
    return 1
}

# Function to speak using system TTS
speak_system() {
    local text="$1"
    if command -v say &>/dev/null; then
        # macOS
        say -r 200 "$text" &
    elif command -v espeak &>/dev/null; then
        # Linux with espeak
        espeak -s 200 "$text" &
    elif command -v spd-say &>/dev/null; then
        # Linux with speech-dispatcher
        spd-say -r 50 "$text" &
    else
        # Fallback: terminal bell
        echo -e "\a" >/dev/tty 2>/dev/null || true
        echo "[NOTIFICATION] $text" >&2
    fi
}

# Speak function with fallback
speak() {
    local text="$1"
    speak_mcp "$text" || speak_system "$text"
}

# Determine message based on notification type
case "$NOTIFICATION_TYPE" in
    idle_prompt)
        speak "[QUESTION] Claude waiting for your input"
        ;;
    permission_prompt)
        speak "[QUESTION] Claude needs your permission"
        ;;
    stop)
        speak "[DONE] Claude has finished the task"
        ;;
    *)
        # For unknown types, just mention Claude needs attention
        speak "[QUESTION] Claude needs attention: $NOTIFICATION_TYPE"
        ;;
esac

exit 0
