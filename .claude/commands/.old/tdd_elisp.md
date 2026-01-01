<!-- ---
!-- Timestamp: 2025-05-08 19:39:52
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/tdd_elisp.md
!-- --- -->

# Test-Driven Development Workflow Guide for Emacs Claude Code

This guide outlines the test-driven development (TDD) workflow for the emacs-claude-code project, based on the established patterns in the codebase.

## Workflow Steps

### 1. Create Feature Branch

```bash
git checkout develop
git checkout -b feature/<verb>-<object>
```

Example: `feature/implement-project-detection`

### 2. Write Tests First

Create test files in the `tests/` directory following the naming pattern:

```elisp
;; For a new module: ecc-new-feature.el
;; Create: tests/test-ecc-new-feature.el

(require 'ert)
(require 'ecc-dependencies)

;; Basic loadability test
(ert-deftest test-ecc-new-feature-loadable ()
  "Test that ecc-new-feature loads properly."
  (should (featurep 'ecc-new-feature)))

;; Test specific functionalities
(ert-deftest test-ecc-new-feature-function-exists ()
  "Test that specific function exists."
  (should (fboundp 'ecc-new-feature-function)))

;; Test behavior with comprehensive input/output tests
(ert-deftest test-ecc-new-feature-expected-behavior ()
  "Test expected behavior of the feature."
  (let ((test-var nil))
    (unwind-protect
        (progn
          ;; Setup test environment
          ;; Test assertions
          (should (equal (ecc-new-feature-function arg) expected-result)))
      ;; Cleanup
      )))
```

### 3. Verify Test Failure

Run the test to confirm it fails before implementation:

```bash
./run-tests.sh -s tests/test-ecc-new-feature.el
```

This verifies the test correctly checks for functionality that doesn't exist yet.

### 4. Commit Test Files

Commit the test files once they're complete:

```bash
git add tests/test-ecc-new-feature.el
git commit -m "Add tests for new feature"
```

### 5. Implement Functionality

Create the implementation files following the established patterns:

```elisp
;;; -*- coding: utf-8; lexical-binding: t -*-
;;; Author: ywatanabe
;;; Timestamp: <timestamp>
;;; File: /path/to/ecc-new-feature.el

;;; Copyright (C) 2025 Yusuke Watanabe (ywatanabe@alumni.u-tokyo.ac.jp)

;; Required dependencies
(require 'ecc-dependencies)

;; Function implementations
(defun ecc-new-feature-function (arg)
  "Description of what this function does with ARG.

Example:
  (ecc-new-feature-function \"example\")
  ;; => expected output"
  ;; Implementation)

;; Provide the feature
(provide 'ecc-new-feature)

(when (not load-file-name)
  (message "ecc-new-feature.el loaded."
           (file-name-nondirectory
            (or load-file-name buffer-file-name))))
```

### 6. Verify Implementation

Run the tests again to verify the implementation passes:

```bash
./run-tests.sh -s tests/test-ecc-new-feature.el
```

Then run the full test suite to ensure there are no regressions:

```bash
./run-tests.sh
```

### 7. Commit Implementation

Once all tests pass, commit the implementation:

```bash
git add ecc-new-feature.el
git commit -m "Implement new feature"
```

## Key Testing Guidelines

1. **One Assertion Per Test**: Each `ert-deftest` should focus on testing one specific aspect
2. **Clean Test Environment**: Use `unwind-protect` to ensure proper cleanup after tests
3. **Avoid Side Effects**: Tests should not modify global state permanently
4. **Clear Test Names**: Name tests to clearly indicate what they test
5. **Proper Cleanup**: Store original values and restore them in cleanup phase

## Run Tests Options

```bash
# Run all tests
./run-tests.sh

# Run tests with debug output
./run-tests.sh -d

# Run a single test file
./run-tests.sh -s tests/test-ecc-feature.el
```

<!-- EOF -->