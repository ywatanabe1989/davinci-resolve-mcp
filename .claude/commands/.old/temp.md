<!-- ---
!-- Timestamp: 2025-05-09 12:33:55
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/temp.md
!-- --- -->

# Understand the rules, formats, and examples & Memorize them as basic conventions for our work

## Task 1. Understand the rules below:
================================================================================
<!-- ## Custom Bash commands and scripts
 !-- - See `~/.bashrc`, `~/.bash.d/*.src`, `~/.bin/*/*.sh`
 !-- - All `*sh` files should have `-h|--help `option
 !--   - If it is not the case, update the contents.
 !-- - Run all tests: `./run-tests.sh`
 !-- - Run tests with debug output: `./run-tests.sh -d` 
 !-- - Run a single test: `./run-tests.sh -s tests/test-ecc-variables.el` -->

<!-- ## Elisp Coding Style
 !-- 
 !-- - Use umbrella structure with up to 1 depth
 !-- - Entry Script
 !--   - Add load-path to the child, umbrella directories
 !--   - Entry file should be `project-name.el`; project-name is the same as the repository root directory name
 !-- - Use kebab-case for filenames, function names, and variable names
 !-- - Other than entry, use acyronym as prefix
 !--   - e.g., `emacs-claude-code/emacs-claude-code.el` and `ecc-*.el` modules, `ecc-*` functions and variables
 !-- - Use `--` prefix for internal functions and variables
 !--   - e.g., `--ecc-internal-function`, `ecc-internal-variable`
 !-- - Function naming: `<package-prefix>-<category>-<verb>-<noun> pattern`
 !--   - e.g., `ecc-buffer-verify-buffer`
 !-- - Include comprehensive docstrings for all functions -->

# Programming Elisp Rules

<!-- - Ensure the number and locations of parentheses are correct.
 !-- - Docstyle Example:
 !--   ```elisp
 !--   (defun elmo-load-json-file (json-path)
 !--     "Load JSON file at JSON-PATH by converting to markdown first.
 !-- 
 !--   Example:
 !--     (elmo-load-json-file \"~/.emacs.d/elmo/prompts/example.json\")
 !--     ;; => Returns markdown content from converted JSON"
 !--     (let ((md-path (concat (file-name-sans-extension json-path) ".md")))
 !--       (when (elmo-json-to-markdown json-path)
 !--         (elmo-load-markdown-file md-path))))
 !--   ``` -->

<!-- EOF -->