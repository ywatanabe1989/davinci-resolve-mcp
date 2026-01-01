#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-29 07:00:54 (ywatanabe)"
# File: ./.claude/to_claude/hooks/notification/notify_voice.sh

ORIG_DIR="$(pwd)"
THIS_DIR="$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)"
LOG_PATH="$THIS_DIR/.$(basename $0).log"
echo > "$LOG_PATH"

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"

GRAY='\033[0;90m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo_info() { echo -e "${GRAY}INFO: $1${NC}"; }
echo_success() { echo -e "${GREEN}SUCC: $1${NC}"; }
echo_warning() { echo -e "${YELLOW}WARN: $1${NC}"; }
echo_error() { echo -e "${RED}ERRO: $1${NC}"; }
echo_header() { echo_info "=== $1 ==="; }
# ---------------------------------------

#!/usr/bin/env bash
# Description: Voice notification when Claude needs attention (Notification hook)

# Notification types:
#   - idle_prompt: Claude is waiting for input
#   - permission_prompt: Claude needs permission

# Uses scitex-audio MCP server (ElevenLabs backend at 1.5x speed)
# Fallback: gTTS, say (macOS), espeak (Linux), or terminal bell

set -euo pipefail

INPUT=$(cat)

NOTIFICATION_TYPE=$(echo "$INPUT" | python3 -c "import json, sys
d = json.load(sys.stdin)
print(d.get('notification_type', '') or '')" 2>/dev/null || echo "")

[ -n "$NOTIFICATION_TYPE" ] || exit 0

PROJECT_NAME=""
BRANCH_NAME=""
if git rev-parse --is-inside-work-tree &>/dev/null; then
    GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "")
    if [ -n "$GIT_ROOT" ]; then
        PROJECT_NAME=$(basename "$GIT_ROOT")
    fi
    BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
fi

PROJECT_PREFIX=""
if [ -n "$PROJECT_NAME" ]; then
    PROJECT_PREFIX="$PROJECT_NAME"
    if [ -n "$BRANCH_NAME" ]; then
        PROJECT_PREFIX="$PROJECT_PREFIX on $BRANCH_NAME"
    fi
    PROJECT_PREFIX="$PROJECT_PREFIX: "
fi

speak_mcp() {
    local text="$1"

    python3 -c "import sys
try:
    from scitex.audio import speak
    speak('$text', speed=1.5, backend='elevenlabs', wait=False)
except Exception:
    try:
        from scitex.audio import speak
        speak('$text', speed=1.5, backend='gtts', wait=False)
    except Exception:
        sys.exit(1)" 2>/dev/null && return 0

    return 1
}

speak_system() {
    local text="$1"

    if command -v say &>/dev/null; then
        say -r 200 "$text" &
    elif command -v espeak &>/dev/null; then
        espeak -s 200 "$text" &
    elif command -v spd-say &>/dev/null; then
        spd-say -r 50 "$text" &
    else
        echo -e "\a" >/dev/tty 2>/dev/null || true
        echo "[NOTIFICATION] $text" >&2
    fi
}

speak() {
    local text="$1"
    speak_mcp "$text" || speak_system "$text"
}

case "$NOTIFICATION_TYPE" in
    idle_prompt)
        speak "${PROJECT_PREFIX}Claude needs your input"
        ;;
    permission_prompt)
        speak "${PROJECT_PREFIX}Claude needs permission"
        ;;
    stop)
        speak "${PROJECT_PREFIX}Task completed"
        ;;
    *)
        speak "${PROJECT_PREFIX}Claude needs attention"
        ;;
esac

exit 0

# EOF