#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-18 19:08:02 (ywatanabe)"
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

#!/usr/bin/env bash
# Description: Check file size limits before Write/Edit (PreToolUse hook)
#
# Thresholds (lines):
#   - py, ts, tsx, js, el: 256
#   - css: 512
#   - html: 1024
#
# Exit codes:
#   0 = OK (proceed)
#   2 = Violation (block and feedback to Claude)

set -euo pipefail

# Read hook input JSON from stdin
INPUT=$(cat)

# Extract file_path and content from hook input
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', '') or '')
" 2>/dev/null || echo "")

CONTENT=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('content', '') or '')
" 2>/dev/null || echo "")

# If no file path, nothing to check
[ -n "$FILE_PATH" ] || exit 0

# Define thresholds by extension
get_threshold() {
    local ext="${1##*.}"
    case "$ext" in
        py|el|sh|src) echo 256 ;;
        ts|tsx|js|jsx|css) echo 512 ;;
        html|htm) echo 1024 ;;
        *) echo "" ;;  # Not managed
    esac
}

THRESHOLD=$(get_threshold "$FILE_PATH")

# If extension not managed, allow
[ -n "$THRESHOLD" ] || exit 0

# Count lines in content (for PreToolUse, content is what will be written)
if [ -n "$CONTENT" ]; then
    LINE_COUNT=$(echo "$CONTENT" | wc -l | tr -d ' ')
else
    # Fallback: check existing file if no content provided
    if [ -f "$FILE_PATH" ]; then
        LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
    else
        exit 0  # New file with no content yet
    fi
fi

# Check threshold
if [ "$LINE_COUNT" -gt "$THRESHOLD" ]; then
    EXT="${FILE_PATH##*.}"
    echo "File size violation: $FILE_PATH" >&2
    echo "  Lines: $LINE_COUNT (max: $THRESHOLD for .$EXT files)" >&2
    echo "" >&2
    echo "Rules:" >&2
    echo "  - py/el/sh/src: max 256 lines" >&2
    echo "  - ts/tsx/js/jsx/css: max 512 lines" >&2
    echo "  - html/htm: max 1024 lines" >&2
    echo "" >&2
    echo "Action required:" >&2
    echo "  1. Document context in ./REFACTORING.md" >&2
    echo "  2. Plan refactoring:" >&2
    echo "     - Design logical module hierarchy" >&2
    echo "     - Keep orchestrator layer thin" >&2
    echo "     - Document plan in ./REFACTORING.md" >&2
    echo "  3. Execute refactoring immediately" >&2
    echo "  4. Delete ./REFACTORING.md after completion" >&2
    echo "  5. Resume original task" >&2
    exit 2
fi

exit 0

# EOF