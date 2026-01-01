#!/bin/bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-18 19:09:22 (ywatanabe)"
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

get_threshold() {
    local ext="${1##*.}"
    case "$ext" in
        py|el|sh|src) echo $THRESHOLD_SMALL ;;
        ts|tsx|js|jsx|css) echo $THRESHOLD_MEDIUM ;;
        html|htm) echo $THRESHOLD_LARGE ;;
        *) echo "" ;;
    esac
}

THRESHOLD=$(get_threshold "$FILE_PATH")

[ -n "$THRESHOLD" ] || exit 0

if [ -n "$CONTENT" ]; then
    LINE_COUNT=$(echo "$CONTENT" | wc -l | tr -d ' ')
else
    if [ -f "$FILE_PATH" ]; then
        LINE_COUNT=$(wc -l < "$FILE_PATH" | tr -d ' ')
    else
        exit 0
    fi
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