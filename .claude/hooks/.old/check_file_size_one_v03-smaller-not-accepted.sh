#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-18 19:51:22 (ywatanabe)"
# File: .//home/ywatanabe/.claude/to_claude/hooks/check_file_size_one.sh

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

echo >"$LOG_PATH"

NC='\033[0m'

#!/usr/bin/env bash

set -euo pipefail

THRESHOLD_SMALL=256
THRESHOLD_MEDIUM=512
THRESHOLD_LARGE=1024
REFACTORING_MD="./REFACTORING.md"

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', '') or '')" 2>/dev/null || echo "")

CONTENT=$(echo "$INPUT" | python3 -c "import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('content', '') or '')" 2>/dev/null || echo "")

[ -n "$FILE_PATH" ] || exit 0

# Get old_string and new_string for Edit tool
OLD_STRING=$(echo "$INPUT" | python3 -c "import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('old_string', '') or '')" 2>/dev/null || echo "")

NEW_STRING=$(echo "$INPUT" | python3 -c "import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('new_string', '') or '')" 2>/dev/null || echo "")

get_threshold() {
    local ext="${1##*.}"
    case "$ext" in
    py | el | sh | src) echo $THRESHOLD_SMALL ;;
    ts | tsx | js | jsx | css) echo $THRESHOLD_MEDIUM ;;
    html | htm) echo $THRESHOLD_LARGE ;;
    *) echo "" ;;
    esac
}

THRESHOLD=$(get_threshold "$FILE_PATH")

[ -n "$THRESHOLD" ] || exit 0

# Get current file size
CURRENT_LINE_COUNT=0
if [ -f "$FILE_PATH" ]; then
    CURRENT_LINE_COUNT=$(wc -l <"$FILE_PATH" | tr -d ' ')
fi

# Calculate new line count based on tool type
if [ -n "$CONTENT" ]; then
    # Write tool: content is the new file content
    LINE_COUNT=$(echo "$CONTENT" | wc -l | tr -d ' ')
elif [ -n "$OLD_STRING" ]; then
    # Edit tool: calculate new size = current - old_lines + new_lines
    OLD_LINES=$(echo "$OLD_STRING" | wc -l | tr -d ' ')
    NEW_LINES=$(echo "$NEW_STRING" | wc -l | tr -d ' ')
    LINE_COUNT=$((CURRENT_LINE_COUNT - OLD_LINES + NEW_LINES))
else
    # No content and no edit - check current file
    if [ -f "$FILE_PATH" ]; then
        LINE_COUNT=$CURRENT_LINE_COUNT
    else
        exit 0
    fi
fi

# Allow edits that reduce file size (even if still over threshold)
if [ "$LINE_COUNT" -lt "$CURRENT_LINE_COUNT" ] && [ "$CURRENT_LINE_COUNT" -gt "$THRESHOLD" ]; then
    # File is over limit but edit reduces size - allow it
    exit 0
fi

if [ "$LINE_COUNT" -gt "$THRESHOLD" ]; then
    EXT="${FILE_PATH##*.}"
    echo "File size violation: $FILE_PATH" >&2
    echo "  Lines: $LINE_COUNT (max: $THRESHOLD for .$EXT files)" >&2
    echo "" >&2
    echo "Rules:" >&2
    echo "  - py/el/sh/src: max $THRESHOLD_SMALL lines" >&2
    echo "  - ts/tsx/js/jsx/css: max $THRESHOLD_MEDIUM lines" >&2
    echo "  - html/htm: max $THRESHOLD_LARGE lines" >&2
    echo "" >&2
    echo "Action required:" >&2
    echo "  1. Document context in $REFACTORING_MD" >&2
    echo "  2. Plan refactoring:" >&2
    echo "     - Design logical module hierarchy" >&2
    echo "     - Keep orchestrator layer thin" >&2
    echo "     - Document plan in $REFACTORING_MD" >&2
    echo "  3. Execute refactoring immediately" >&2
    echo "  4. Delete $REFACTORING_MD after completion" >&2
    echo "  5. Resume original task" >&2
    exit 2
fi

exit 0

# EOF