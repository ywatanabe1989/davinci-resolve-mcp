#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# Timestamp: "2025-12-18 (ywatanabe)"
# File: ~/.claude/to_claude/hooks/run_lint.sh
# Description: Run linters with auto-fix after Write/Edit (PostToolUse hook)
#
# Supported languages:
#   - Python: ruff check --fix (or flake8 as fallback)
#   - TypeScript/JavaScript: eslint --fix
#   - Emacs Lisp: byte-compile
#   - Shell: shellcheck
#   - HTML: htmlhint
#
# Exit codes:
#   0 = Success
#   1 = Warning (Claude sees feedback but continues)
#   2 = Error (Claude must fix)

set -euo pipefail

# Add tool paths if they exist
NPM_GLOBAL_BIN="$HOME/.npm-global/bin"
LOCAL_BIN="$HOME/.local/bin"
GOPATH_BIN="$(go env GOPATH 2>/dev/null || true)/bin"

[ -d "$NPM_GLOBAL_BIN" ] && export PATH="$NPM_GLOBAL_BIN:$PATH"
[ -d "$LOCAL_BIN" ] && export PATH="$LOCAL_BIN:$PATH"
[ -d "$GOPATH_BIN" ] && export PATH="$GOPATH_BIN:$PATH"

# Read hook input JSON from stdin
INPUT=$(cat)

# Extract file_path from hook input
FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('tool_input', {}).get('file_path', '') or '')
" 2>/dev/null || echo "")

# If no file path or file doesn't exist, nothing to lint
[ -n "$FILE_PATH" ] || exit 0
[ -f "$FILE_PATH" ] || exit 0

lint_python() {
    local file="$1"
    if command -v ruff &>/dev/null; then
        ruff check --fix "$file" 2>&1 || true
    elif command -v flake8 &>/dev/null; then
        flake8 "$file" 2>&1 || true
    fi
}

lint_js_ts() {
    local file="$1"
    if command -v eslint &>/dev/null; then
        eslint --fix "$file" 2>&1 || true
    fi
}

lint_elisp() {
    local file="$1"
    # Check for common Emacs Lisp issues using emacs batch mode
    if command -v emacs &>/dev/null; then
        # Basic syntax check via byte-compilation
        emacs --batch \
            --eval "(setq byte-compile-error-on-warn t)" \
            --eval "(byte-compile-file \"$file\")" \
            2>&1 || true
        # Clean up .elc file
        rm -f "${file}c" 2>/dev/null || true
    fi
}

lint_shell() {
    local file="$1"
    if command -v shellcheck &>/dev/null; then
        shellcheck "$file" 2>&1 || true
    fi
}

lint_html() {
    local file="$1"
    if command -v htmlhint &>/dev/null; then
        htmlhint "$file" 2>&1 || true
    fi
}

# Lint based on file extension
case "$FILE_PATH" in
*.py)
    lint_python "$FILE_PATH"
    ;;
*.ts | *.tsx | *.js | *.jsx)
    lint_js_ts "$FILE_PATH"
    ;;
*.el)
    lint_elisp "$FILE_PATH"
    ;;
*.sh | *.src | *.bash)
    lint_shell "$FILE_PATH"
    ;;
*.html | *.htm)
    lint_html "$FILE_PATH"
    ;;
esac

exit 0
