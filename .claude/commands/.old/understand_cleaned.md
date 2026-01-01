<!-- ---
!-- Timestamp: 2025-05-09 10:22:22
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/understand_.md
!-- --- -->

# Programming Guidelines & Standards

## Table of Contents
- [General Programming Rules](#general-programming-rules)
- [Project Structure](#project-structure)
- [Language-Specific Rules](#language-specific-rules)
  - [Python](#python-rules)
  - [Shell](#shell-script-rules)
  - [Elisp](#elisp-rules)
- [Documentation Standards](#documentation-standards)
- [Testing Framework](#testing-framework)
- [Project Management](#project-management)
- [MNGS Framework](#mngs-framework)
- [Format Examples](#format-examples)
- [Test-Driven Development Workflow](#test-driven-development-workflow)

## General Programming Rules

- **Focus on code clarity and maintainability**
  - Do Not Repeat Yourself (DRY principle)
  - Use symbolic links wisely, especially for large data to keep clear organization and easy navigation
  - Prepare `./scripts/utils/<versatile_func.py>` for versatile and reusable code
  - If versatile code is applicable beyond projects, implement in the `mngs` package
  - Avoid unnecessary comments as they can be disruptive
  - Return only the updated code without comments
  - Code should be self-explanatory; variable, function, and class names are crucial
  - Comments can be distracting if the code is properly written

- **Avoid 1-letter variable names**
  - They make searching challenging
  - For example, rename variable x to xx for better readability, writability, and searchability

- **Commenting style**
  - Subjects of comments should be "this file/code/function" implicitly
  - Verbs should be in singular form (e.g., "# Computes ..." instead of "# Compute ...")

- **Documentation**
  - Always include docstrings with example usage
  - Follow language-specific docstring format standards

- **Imports and Dependencies**
  - Keep importing packages MECE (Mutually Exclusive and Collectively Exhaustive)
  - Remove unnecessary packages and add necessary ones

- **Code Structure**
  - Use modular approaches for reusability, readability, and maintainability
  - Split functions into subroutines or meaningful chunks whenever possible

- **PATH Conventions**
  - Use relative paths from the project root
  - Relative paths should start with dots, like "./relative/example.py" or "../relative/example.txt"
  - All scripts are assumed to be executed from the project root (e.g., ./scripts/example.sh)

- **Code Block Indicators**
  - Use appropriate code block indicators:
  ```python
  # Python example
  ```
  ```shell
  # Shell example
  ```
  ```elisp
  ;; Elisp example
  ```

- **String Formatting**
  - Split strings into shorter lines
  - For example, with f-string concatenation with parentheses in Python:
  ```python
  # Good
  error_msg = (
      f"Failed to parse JSON response: {error}\n"
      f"Prompt: {self._ai_prompt}\n"
      f"Generated command: {commands}\n"
      f"Response: {response_text}"
  )
  
  # Not Good
  error_msg = f"Failed to parse JSON response: {error}\nPrompt: {self._ai_prompt}\nGenerated command: {commands}\nResponse: {response_text}"
  ```

- **Headers and Footers**
  - Do not change headers (e.g., time stamp, file name, authors) and footers (e.g., # EOF)

- **Indentation**
  - Pay attention to indentation
  - Code will be copied/pasted as is

## Project Structure

### Directory Structure
```
<project root>
|-- .git
|-- .gitignore
|-- .env
|   `-- bin
|       |-- activate
|       `-- python
|-- config
|   |-- <file_name>.yaml
|   |-- <file_name>.yaml
|   |...
|   `-- <file_name>.yaml
|-- data
|   `-- <dir_name>
|        |-- <file_name>.npy -> ../../scripts/path/to/script/script_name_out/<file_name>.npy
|        |-- <file_name>.txt -> ../../scripts/path/to/script/script_name_out/<file_name>.txt
|        |-- <file_name>.csv -> ../../scripts/path/to/script/script_name_out/<file_name>.csv
|        |...
|        `-- <file_name>.mat -> ../../scripts/path/to/script/script_name_out/<file_name>.mat
|-- project_management
|   |-- original_plan.md
|   |-- progress.md 
|   |-- progress.mmd
|   |-- progress.gif
|   `-- progress.svg
|-- README.md
|-- requirements.txt
`-- scripts
    `-- <OLD-TIMESTAMP>-<title>
        |-- NNN_<script_name>.py
        |-- NNN_<script_name>_out/<file_name>.npy
        |-- NNN_<script_name>_out/<file_name>.txt
        |-- NNN_<script_name>_out/<file_name>.csv
        `-- run_all.sh
```

### Directory Purpose
- **`./.env`**: Python environment for the project (may be symlinked to shared env)
- **`./.git`**: Git directory
- **`./config`**: Centralized YAML configuration files shared in the project
- **`./data`**: Centralized data files, symbolic links to actual files in scripts
- **`./project_management`**: Project management files
- **`./scripts`**: Executable files (.py, .sh), their output files and logs

### Configuration Files
- Store in `./config` in YAML format (e.g., `./config/PATH.yaml`)
- In Python, `CONFIG` variable concatenates YAML files
- f-strings are acceptable in config YAML files

## Language-Specific Rules

### Python Rules

#### General Python Rules
- Do not use try-except blocks as much as possible (makes debugging challenging with invisible errors)
- Ensure indent level matches with input
- Do not change the header of python files:
  ```python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  # Time-stamp: \"%s (%s)\"
  # %s
  ```
- Do not change commenting lines in python scripts:
  - """Imports"""
  - """Parameters"""
  - """Functions & Classes"""

- Use `argparse` even when no arguments are necessary
  - Every python file should have at least one argument: -h|--help
- Always use `main` guard:
  ```python
  if __name__ == "__main__":
      main()
  ```
- Adopt modular approaches with smaller functions
- Implement Python logging (instead of print statements):
  ```python
  import logging
  logging.error()
  logging.warning() 
  logging.info()
  logging.debug()
  ```
  - Replace print statements: `print()` -> `logging.info()`
  - Progress tracking: 
    - `from tqdm import tqdm`
    - `progress_bar = tqdm(total=100)`
  - Debug tracing:
    - `from icecream import ic`
    - `ic()` for variable inspection

- Format integer numbers with underscores (e.g., 100_000)
- Display integers with commas (e.g., 100,000)
- Fix random seed as 42

- Naming conventions:
  - Variable names in scripts:
    - lpath(s) - load paths
    - ldir - load directory
    - spath(s) - save paths
    - sdir - save directory
    - path(s) - generic paths
    - fname - file name
  - Directory names should be noun forms: e.g., mnist-creation/, mnist-classification/
  - Script file name should start with verb if it expects inputs and produces outputs
  - Definition files for classes should be Capital: ClassName.py
  - Predefined parameters must be written in uppercase letters: PARAM

#### Python Type Hints
- Explicitly define variable types in functions and classes
  ```python
  from typing import Union, Tuple, List, Dict, Any, Optional, Callable
  from collections.abc import Iterable
  ArrayLike = Union[List, Tuple, np.ndarray, pd.Series, pd.DataFrame, xr.DataArray, torch.Tensor]
  ```

#### Python Docstring Format
```python
def func(arg1: int, arg2: str) -> bool:
    """Summary line.

    Extended description of function.

    Example
    ----------
    >>> xx, yy = 1, "test"
    >>> out = func(xx, yy)
    >>> print(out)
    True

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    """
    return True
```

#### Top-level Docstring Format
```python
"""
1. Functionality:
   - (e.g., Executes XYZ operation)
2. Input:
   - (e.g., Required data for XYZ)
3. Output:
   - (e.g., Results of XYZ operation)
4. Prerequisites:
   - (e.g., Necessary dependencies for XYZ)

(Remove me: Please fill docstrings above, while keeping the bullet point style, and remove this instruction line)
"""
```

#### Function Hierarchy Separators
```python
# 1. Main entry point
# ---------------------------------------- 


# 2. Core functions
# ---------------------------------------- 


# 3. Helper functions
# ---------------------------------------- 
```

#### Python Statistics Rules
- Report statistical results with p-value, stars, sample size, effect size, test name, statistic, and null hypothesis
- Use `mngs.stats.p2stars` for p-values with stars
- Implement FDR correction for multiple comparisons
- Round statistical values by factor 3 (.3f format)
- Write statistical values in italic font (e.g., \textit{n})

### Shell Script Rules

- Include one-line explanation for function, followed by example usage
- Ensure if-fi syntaxes are correct
- Include argument parser and usage (with -h|--help option)
- Include logging functionality

#### Shell Script Template
```bash
#!/bin/bash
# script-name.sh
# Author: ywatanabe (ywatanabe@alumni.u-tokyo.ac.jp)
# Date: $(date +"%Y-%m-%d-%H-%M")

LOG_FILE=".$0.log" # Do not remove existing extension (e.g., script.sh.log is preferred)

usage() {
    echo "Usage: $0 [-s|--subject <subject>] [-m|--message <message>] [-h|--help]"
    echo
    echo "Options:"
    echo "  -s, --subject   Subject of the notification (default: 'Subject')"
    echo "  -m, --message   Message body of the notification (default: 'Message')"
    echo "  -h, --help      Display this help message"
    echo
    echo "Example:"
    echo "  $0 -s \"About the Project A\" -m \"Hi, ...\""
    echo "  $0 -s \"Notification\" -m \"This is a notification from ...\""
    exit 1
}

my-echo() {
  while [[ $# -gt 0 ]]; do
      case $1 in
          -s|--subject)
              subject="$1"
              shift 1
              ;;
          -m|--message)
              shift
              message="$1"
              shift
              ;;
          -h|--help)
              usage
              ;;
          *)
              echo "Unknown option: $1"
              usage
              ;;
      esac
  done

  echo "${subject:-Subject}: ${message:-Message} (Yusuke Watanabe)"
}

main() {
    my-echo "$@"
}

main "$@" 2>&1 | tee "$LOG_FILE"

notify -s "$0 finished" -m "$0 finished"

# EOF
```

#### Run All Script Template
```bash
#!/bin/bash
# Timestamp: "2025-01-18 06:47:46 (ywatanabe)"
# File: ./scripts/<timestamp>-<title>/run_all.sh

LOG_FILE="$0%.log"

usage() {
    echo "Usage: $0 [-h|--help]"
    echo
    echo "Options:"
    echo " -h, --help   Display this help message"
    echo
    echo "Example:"
    echo " $0"
    exit 1
}

main() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help) usage ;;
              -) echo "Unknown option: $1"; usage ;;
        esac
    done
    
    commands=(
        "./scripts/<timestamp>-<title>/001_filename1.py"
        "./scripts/<timestamp>-<title>/002_filename2.py" 
        "./scripts/<timestamp>-<title>/003_filename3.py"
    )

    for command in "${commands[@]}"; do
        echo "$command"
        eval "$command"
        if [[ $? -ne 0 ]]; then
            echo "Error: $command failed."
            return 1
        fi
    done

    echo "All scripts finished successfully."
    return 0
}

{ main "$@"; } 2>&1 | tee "$LOG_FILE"
```

### Elisp Rules

#### Elisp Coding Style
- Use umbrella structure with up to 1 depth
- Entry script should add load-path to child directories
- Entry file should be `project-name.el`
- Use kebab-case for filenames, function names, and variable names
- Use acronym as prefix for non-entry files (e.g., `ecc-*.el`)
- Use `--` prefix for internal functions and variables
- Function naming: `<package-prefix>-<category>-<verb>-<noun>` pattern
- Include comprehensive docstrings

#### Elisp Function Hierarchy Separators
```elisp
;; 1. Main entry point
;; ---------------------------------------- 


;; 2. Core functions
;; ---------------------------------------- 


;; 3. Helper functions
;; ---------------------------------------- 
```

## Documentation Standards

### Docstrings
- Always include examples in docstrings
- Ensure docstrings follow language-specific format
- For Python functions, use NumPy-style docstrings
- For Python scripts, use custom top-level docstring format

### Comments
- Keep comments minimal but meaningful
- Use comments for section separation and clarification
- Avoid redundant comments that just restate code

## Test-Driven Development Workflow

1. **Start with tests**
   - We're following test-driven development 
   - Write tests before writing source code
   - Write tests based on expected input/output pairs
   - Avoid mock implementations
   - Tests should target functionality that doesn't exist yet
   - Implement `./run-tests.sh` with these options:
     ```
     -d|--debug     Enable debug output. <- DO NOT USE this unless explicitly requested
     -h|--help      Display this help message"
     -s|--single    Run a single test file"
     ```
   - Prioritize test over source
     - The quality of test is the quality of the project
   - Test code should have the expected directory structure in the language and project goals

2. **Verify test failure**
   - Run the tests to confirm they fail first
     - Our aim is now clear; all we need is to solve the failed tests
   - Not to write implementation code yet

3. **Git commit test files**
   - Review the tests for completeness to satisfy the project goals and requirements
     - Not determine the qualities of test files based on source files
       - Prioritize test code over source code
       - Thus, test code MUST BE SOLID
   - Commit the tests when satisfied

4. **Implement functionality**
   - If the above steps 1-3 completed, now you are allowed to implement source code that passes the tests
   - !!! IMPORTANT !!! NOT TO MODIFY THE TEST FILES IN THIS STEP
   - Iterate until all tests pass

5. **Verify implementation quality**
   - Use independent subagents to check if implementation overfits to tests
   - Ensure solution meets broader requirements beyond tests

6. **Summarize the current iteration by listing:**
   - What were verified
   - What are not verified yet
     - Reasons why they are not verified if not expected

7. **Commit implementation**
   - Commit the source code once satisfied

## Testing Framework Rules

### Python Testing
- DO NOT USE UNITTEST
- USE PYTEST
- Prepare pytest.ini
- Structure:
  - ./src/project-name/__init__.py
  - ./tests/project-name/...
- Each test function should be smallest
- Each test file contain only one test function
- Each Test Class should be defined in a dedicated script
- Test codes MUST BE MEANINGFUL
- Implement run_tests.sh (or run_tests.ps1 for projects which only works on Windows) in project root

### Elisp Testing
- Test codes will be executed after loading all environments and in the run time environment
  - Therefore, do not change variables for testing purposes
  - Check whether codes are working in the variables defined in run time code
  - DO NOT SETQ/DEFVAR/DEFCUSTOM ANYTHING
  - DO NOT LET/LET* TEST VARIABLES
  - DO NOT LOAD ANYTHING
  - If source scripts are provided, create corresponding test files in a one-by-one manner, adding test- prefix to source scripts filenames
  - Split test code into smallest blocks
    - Each ert-deftest should include only one should or should-not
  - Test codes MUST BE MEANINGFUL

- To check if require statement is valid, use this format IN A ENTRY FILE:
  ```elisp
  (require 'ert)

  (ert-deftest test-lle-with-loadable
      ()
    (require 'lle-with)
    (should
     (featurep 'lle-with)))

  (ert-deftest test-lle-with-system-root-loadable
      ()
    (require 'lle-with-system-root)
    (should
     (featurep 'lle-with-system-root)))

  (ert-deftest test-lle-with-project-root-loadable
      ()
    (require 'lle-with-project-root)
    (should
     (featurep 'lle-with-project-root)))
  ```
  - Loadable tests should not be split across files but concentrate on central entry files
  - Ensure the codes identical between before and after testing; implement cleanup process
  - DO NOT ALLOW CHANGE DUE TO TEST
  - When edition is required for testing, first store original information and revert in the cleanup stage

## Project Management

### Progress Rules
- Direction of the project is managed under `./project_management`
- Main file: `./project_management/progress.md`
  - Main progress management file. Update this as project advances.
  - Use tags:
    - TODO
      - Format: `[ ] contents`
      - For contents that need to be addressed or completed.
    - DONE
      - Format: `[x] contents`
      - Fill checkbox
      - For contents that have been completed (considered as done by agents).
    - JUSTIFICATION
      - Format: `__justification__ | contents`
      - References to justify why you determine the contents are DONE
    - ACCEPTED
      - Format: `__accepted__ | contents`
      - For contents accepted by the user.
      - Note: Only users can add or remove this tag.
    - REJECTED
      - Format: `~~contents~~`
      - For contents rejected by the user.
      - Note: Only users can add or remove this tag.
    - SUGGESTION
      - Format: `__suggestions__ | contents`
      - For contents suggested by agents.

- Supporting files:
  - `./project_management/progress.mmd`
    - Mermaid diagram definition reflecting the current progress
    - Use tags as well
  - `./project_management/progress.svg`
    - SVG file created from the mermaid file
  - `./project_management/progress.gif`
    - GIF image created from the SVG file
  - `./project_management/ORIGINAL_PLAN.md`
    - Original plan created by the user
    - DO NOT EDIT THIS FILE

## MNGS Framework

### Overview
- Custom Python utility package for standardizing scientific analyses
- Features predefined directory structure and conventions
- Manages configuration, environment, and file organization

### Python MNGS Format
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "2024-11-03 10:33:13 (ywatanabe)"
# File: placeholder.py

__file__ = "placeholder.py"

"""
Functionalities:
  - Does XYZ
  - Does XYZ
  - Does XYZ
  - Saves XYZ

Dependencies:
  - scripts:
    - /path/to/script1
    - /path/to/script2
  - packages:
    - package1
    - package2
IO:
  - input-files:
    - /path/to/input/file.xxx
    - /path/to/input/file.xxx

  - output-files:
    - /path/to/input/file.xxx
    - /path/to/input/file.xxx
"""

"""Imports"""
import os
import sys
import argparse

"""Warnings"""
# mngs.pd.ignore_SettingWithCopyWarning()
# warnings.simplefilter("ignore", UserWarning)
# with warnings.catch_warnings():
#     warnings.simplefilter("ignore", UserWarning)

"""Parameters"""
# from mngs.io import load_configs
# CONFIG = load_configs()

"""Functions & Classes"""
def main(args):
    pass

import argparse
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    import mngs
    script_mode = mngs.gen.is_script()
    parser = argparse.ArgumentParser(description='')
    args = parser.parse_args()
    mngs.str.printc(args, c='yellow')
    return args

def run_main() -> None:
    """Initialize mngs framework, run main function, and cleanup.

    mngs framework manages:
      - Parameters defined in yaml files under `./config dir`
      - Setting saving directory (/path/to/file.py -> /path/to/file.py_out/)
      - Symlink for `./data` directory
      - Logging timestamp, stdout, stderr, and parameters
      - Matplotlib configurations (also, `mngs.plt` will track plotting data)
      - Random seeds

    THUS, DO NOT MODIFY THIS RUN_MAIN FUNCTION
    """
    global CONFIG, CC, sys, plt

    import sys
    import matplotlib.pyplot as plt
    import mngs

    args = parse_args()

    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(
        sys,
        plt,
        args=args,
        file=__file__,
        sdir_suffix=None,
        verbose=False,
        agg=True,
    )

    exit_status = main(args)

    mngs.gen.close(
        CONFIG,
        verbose=False,
        notify=False,
        message="",
        exit_status=exit_status,
    )

if __name__ == '__main__':
    run_main()

# EOF
```

### Key MNGS Functions
- **`mngs.gen.start(...)`** - Initialize environment (might be better to handle automatically using hook)
- **`mngs.gen.close(...)`** - Clean up environment (might be better to handle automatically using hook)
- **`mngs.io.load_configs()`** - Load YAML files under ./config as a dot-accessible dictionary
  - Centralize variables here (paths in PATH.yaml, project-specific params in project.yaml)
- **`mngs.io.load()`** - Load data using relative path from project root
  - Ensure to load from (symlinks of) `./data` directory, not from `./scripts`
  - Use CONFIG.PATH.... to specify paths
- **`mngs.io.save(obj, spath, symlink_from_cwd=True)`** - Save with automatic format handling
  - From the extension of spath, saving code will be handled automatically
  - Note that save path must be relative to use symlink_from_cwd=True
  - Organize data (and symlinks) under the ./data directory
- **`mngs.plt.subplots(ncols=...)`** - Matplotlib wrapper that tracks plotting data
  - Plotted data will be saved in CSV with the same name as the figure
  - CSV file will be the same format expected in plotting software SigmaPlot
- **`mngs.str.printc(message, c='blue')`** - Colored console output
  - Acceptable colors: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey'
  - Default is None, which means no color
- **`mngs.stats.p2stars(p_value)`** - Convert p-values to significance stars
- **`mngs.stats.fdr_correction(results)`** - Apply FDR correction for multiple comparisons
- **`mngs.pd.round(df, factor=3)`** - Round numeric values in dataframe with specified precision

## Format Examples

### YAML Configuration Example
```yaml
# Time-stamp: "2025-01-18 00:00:34 (ywatanabe)"
# File: ./config/COLORS.yaml

COLORS:
  SEIZURE_TYPE:
    "1": "red"
    "2": "orange"
    "3": "pink"
    "4": "gray"

COLORS:
  "interictal_control": "blue"
  "abnormal discharge": "yellow"
  "seizure-like event": "orange"
  "seizure": "red"
```

### Project Management Format
```
* Title

| Type | Stat | Description       | User |
|------|------|-------------------|------|
| 🚀 T | [x]  | Potential Title 1 | 👍 A |
|------|------|-------------------|------|
| 🚀 T | [ ]  | Potential Title 2 | 👀 T |

* Goals, Milestones, and Tasks

** 🎯 Goal 1: Description

| Type | Stat | Description                           | User |
|------|------|---------------------------------------|------|
| 🎯 G | [ ]  | Accepted but not completed Goal       | 👍 A |
|------|------|---------------------------------------|------|
| 🏁 M | [ ]  | Accepted but not completed Milestone  | 👍 A |
|------|------|---------------------------------------|------|
| 📋 T | [x]  | Accepted and completed Task           | 👍 A |
|      | [x]  | 📊 `/path/to/data_file.ext`           | 👍 A |
```

### Legend for Project Management
```
| **Type** | **Meaning**               | **Status** | **Meaning** | **User Status** | **Meaning** |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 🚀 T   | Title                   | [ ]      | TODO      | 👀 T          | To see    |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 🔎 H   | Hypothesis              | [x]      | DONE      | ❌ R          | Rejected  |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 🎯 G   | Goal                    |          |           | 👍 A          | Accepted  |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 🏁 M   | Milestone               |          |           |               |           |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 📋 T   | Task                    |          |           |               |           |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 🛠️ T   | Tool (as Justification) |          |           |               |           |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 📊 D   | Data (as Justification) |          |           |               |           |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 📌 J   | File as Justification   |          |           |               |           |
|--------|-------------------------|----------|-----------|---------------|-----------|
| 💡 S   | Suggestion              |          |           |               |           |
```

<!-- EOF -->