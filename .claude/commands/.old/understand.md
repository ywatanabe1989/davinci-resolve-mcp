<!-- ---
!-- Timestamp: 2025-05-08 16:50:19
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/understand.md
!-- --- -->

# Understand

## Task 1. Understand the rules below:
================================================================================
## Custom Bash commands and scripts
- See `~/.bashrc`, `~/.bash.d/*.src`, `~/.bin/*/*.sh`
- All `*sh` files should have `-h|--help `option
  - If it is not the case, update the contents.
- Run all tests: `./run-tests.sh`
- Run tests with debug output: `./run-tests.sh -d` 
- Run a single test: `./run-tests.sh -s tests/test-ecc-variables.el`

## Elisp Coding Style

- Use umbrella structure with up to 1 depth
- Entry Script
  - Add load-path to the child, umbrella directories
  - Entry file should be `project-name.el`; project-name is the same as the repository root directory name
- Use kebab-case for filenames, function names, and variable names
- Other than entry, use acyronym as prefix
  - e.g., `emacs-claude-code/emacs-claude-code.el` and `ecc-*.el` modules, `ecc-*` functions and variables
- Use `--` prefix for internal functions and variables
  - e.g., `--ecc-internal-function`, `ecc-internal-variable`
- Function naming: `<package-prefix>-<category>-<verb>-<noun> pattern`
  - e.g., `ecc-buffer-verify-buffer`
- Include comprehensive docstrings for all functions

# Programming Elisp Rules

- Ensure the number and locations of parentheses are correct.
- Docstyle Example:
  ```elisp
  (defun elmo-load-json-file (json-path)
    "Load JSON file at JSON-PATH by converting to markdown first.

  Example:
    (elmo-load-json-file \"~/.emacs.d/elmo/prompts/example.json\")
    ;; => Returns markdown content from converted JSON"
    (let ((md-path (concat (file-name-sans-extension json-path) ".md")))
      (when (elmo-json-to-markdown json-path)
        (elmo-load-markdown-file md-path))))
  ```

# Programming General Rules

#### PATH
- Use relative path from the project root
- Relative paths should start with dots, like "./relative/example.py" or "../relative/example.txt"
- Use relative paths but full paths are acceptable when admirable
- All Scripts are assumed to be executed from the project root (e.g., ./scripts/example.sh)

- Do Not Repeat Yourself
  - Use symbolic links wisely, especially for large data to keep clear organization and easy navigation
  - Prepare `./scripts/utils/<versatile_func.py>` for versatile and reusable code
    - Then, for example, `from scripts.utils.versatile_func import versatile_func` from main files
  - If versatile code is applicable beyond projects, implement in the `mngs` package, my toolbox
    - `mngs` is in `$HOME/proj/mngs_repo/src/mngs/`
      - It is installed in the `./.env` via a development installation (e.g., `pip install -e $HOME/proj/mngs_repo/`)

- Avoid unnecessary comments as they are disruptive.
	- Return only the updated code without comments.

- DO NOT USE DIFF FORMAT

- Use code block indicators:
  - e.g.,
  - ``` python
    CODE-HERE
    ```
  - ``` pseudo-code
    CODE-HERE
    ```
  - ``` plaintext
    CODE-HERE
    ```
  - ``` prompt
    CODE-HERE
    ```

- String should be split into shorter lines
  - e.g., f-string concatenation with parentheses in python
  - NG
    ``` python
    error_msg = f"Failed to parse JSON response: {error}\nPrompt: {self._ai_prompt}\nGenerated command: {commands}\nResponse: {response_text}"
    ```
  - Good
    ``` python
    error_msg = (
        f"Failed to parse JSON response: {error}\n"
        f"Prompt: {self._ai_prompt}\n"
        f"Generated command: {commands}\n"
        f"Response: {response_text}"
    )
    ```

- Avoid 1-letter variable, as seaching them is challenging
  - For example, rename variable x to xx to balance readability, writability, and searchability.

- Code must be self-explanatory
  - Project structure, variable/function/class names must indicate their roles
  - Ultimately, comments can be just distracting if well-written

- Subjects of comments should be the script/function/code
  - Verbs must be in their singular form:
    - NG: "# Compute's' ..."
    - CORRECT "# Compute ...".

- Always write docstring with example usage

- Long response is acceptable
  - If wards limit reaches, I will ask you "continue" in the next interaction

- Do not change headers (e.g., time stamp, file name, authors) and footers (e.g. # EOF).

- Must pay attention to indents
  - I may copy/paste your revision to my code as is.


## Programming Structure Rules
- Organize directory structure in the format explained below
  - DO NOT CREATE ANY DIRECTORIES IN PROJECT ROOT
  - Creating sub-directories as long as readability increases
  - Hide unnecessary files and directories
  - Organize project structures by moving, hiding, combining files
    - When path changed, ensure to update `./config/PATH.yaml` correspondingly

- Directories in the project root are defined as follows:
  - `./.env`
    - Prepared Python environment for the project
    - May be symlinked to the shared env (`$HOME/.env`)
  - `./.git`
    - Git directory
  - `./config`
    - Centralize YAML configuration files shared in the project
    - Paths and Constant variables must be written here, instead of directly write in scripts
  - `./data`
    - Centralize data files shared in the project
      - Store files other than scripts, such raw data and large files (.npy, .csv, .jpg, and .pth data)
        - However, the outputs of a script should be located close to the script
          - e.g., ./scripts/example.py_out/output.jpg
        - Then, symlinked to `./data` directory
          - e.g., ./scripts/example.py_out/data/output.jpg -> ./data/output.jpg
      - This is useful to link scripts and outputs, while keeping centralized data directory structure
      - Large files under `./scripts` or `./data` are git-ignored
  - `./project-management`
    - Project management files
  - `./scripts`
    - Executable files (.py, .sh), their output files and logs

  - `.gitignore` will ignore large files under `./data` and `./scripts`

  - `./data/`
    - Includes raw data
      - However, if it is downloaded by a script, the entity should be near the script and symbolic link should be added to `./data/` directory
      - The .gitignore file will handle large files under the `./scripts` directory
    - Includes potentially large files (.npy, .csv, .jpg, and .pth data)
    - Includes symbolic linkes to processed data located  under `./scripts`
      - This is helpful for linking processed data and the associated script
    - Is ignored by git via the .gitignore file
      - Add .git-keep for empty directories
  - `./docs/`
    - For document files (.md) for humans
  - `./logs/`
    - Logging files for the project
    - `lle-log-` and `--lle-log-` functions add messages to files for a specific log-level
  - `./project_management/`
    - The project_management.mmd and rendered figures are stored
  - `./reports/`
    - Report files (.org|.pdf)
  - `./scripts/`
    - Executable files (python|shell|elisp) and their logs and outputs

- Use symbolic links wisely
- Common scripts should be reused
- Output data should be placed near the scripts which produces them
  - Symbolic links should be organized in the data directory, referencing to the original file under the scripts directory

- A project should be organized as follows:
  ```plaintext
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

<!-- EOF --><!-- ---
!-- Timestamp: 2025-05-08 13:13:17
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.emacs.d/lisp/emacs-claude-code/.claude/commands/programming-python-project-structure.md
!-- --- -->

- Configuration files should be stored under `./config` in YAML format (e.g., `./config/PATH.yaml`)
- In Python scripts, `CONFIG` variable (= a dot-accessible dict) concatenates YAML files
- f-string are acceptable in config YAML files
  - In Python, eval(CONFIG.VARIABLE.WITH.F.EXPRESSION) works to fill variables
  - Also, f-string are utilized in a custom manner
    - For example, the following line will be used to search and glob data for patient at specific datetime:
      f"./data/mat/Patient_{patient_id}/Data_{year}_{month}_{day}/Hour_{hour}/UTC_{hour}_{minute}_00.mat"

## Programming Python Rules

- Do not use try-except blocks as much as possible. This is because I often struggle with invisible errors for debugging.

- Ensure indent level matches with my input; I will insert your output into my code as is. However, the indents in my input may be corrupted for formatting issues. In that case, please fix them.

- Do not change the header of python files:
  ``` python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  # Time-stamp: \"%s (%s)\"
  # %s

- Update top-level docstring in python files to provide a overview, considering the contents of the file contents. When you don't understand meanings of variables, please ask me simple questions in the first iteration. I will respond to your question and please retry the revision again. This top-level docstring should follow this template, instead of the NumPy style:
  ``` python
  """
  1. Functionality:
     - (e.g., Executes XYZ operation)
  2. Input:
     - (e.g., Required data for XYZ)
  3. Output:
     - (e.g., Results of XYZ operation)
  4. Prerequisites:
     - (e.g., Necessary dependencies for XYZ)

  (Remove me: Please fill docstrings above, while keeping the bulette point style, and remove this instruction line)
  """
  ```

- On the other hand, docstrings for functions and classes should be writte in the NumPy style:
  ``` python
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

- Do not change these commenting lines in python scripts:
  - """Imports"""
  - """Parameters"""
  - """Functions & Classes"""

- Do not skip any lines as much as possible. I am really suprized by your speed and accuracy of coding and appreciate your support and patience.

- My code may include my own Python utility package, mngs. Keep its syntax unchanged.
  - For scripts in mngs package, please import functions using underscore to keep namespace clean (e.g., import numpy as _np).
  - For mngs scripts, please use relative import to reduce dependency (e.g., from ..io._load import load)

- When possible, independently implement reusable functions or classes as I will incorporate them into my mngs toolbox.

- Do not forget explicitly define variable types in functions and classes.
  - Use these types and more:
    ``` python
    from typing import Union, Tuple, List, Dict, Any, Optional, Callable
    from collections.abc import Iterable
    ArrayLike = Union[List, Tuple, np.ndarray, pd.Series, pd.DataFrame, xr.DataArray, torch.Tensor]
    ```
- Implement error handling thoroughly.

- Rename variables if your revision makes it better.

- Keep importing packages MECE (Mutually Exclusive and Collectively Exhaustive). Remove/add unnecessary/necessary packages, respectively.

- In code, integer numbers should be written with an underscore every three digits (e.g., 100_000).
- Integer numbers should be shown (in printing, general text, and output data as csv) with an comma every three digits (e.g., 100,000).

- Use modular approaches for reusability, readability, and maintainability. If functions can be split int subroutines or meaningful chunks, do not hesitate to split into pieces, as much as possible.

## Statistics Rules

- Statistical results must be reported with p value, stars (explained later), sample size or dof, effect size, test name, statistic, and null hypothes as much as possible.
  ``` python
  results = {
       "p_value": pval,
       "stars": mngs.stats.p2stars(pval),
       "n1": n1,
       "n2": n2,
       "dof": dof,
       "effsize": effect_size,
       "test_name": test_name_text,
       "statistic": statistic_value,
       "H0": null_hypothes_text,
  }
  ```
  - So, if you want to use scipy.stats package, do not forget to calculate necessary values listed above.

- P-values should be output with stars using mngs.stats.p2stars:
  ``` python
  # mngs.stats.p2stars
  def p2stars(input_data: Union[float, str, pd.DataFrame], ns: bool = False) -> Union[str, pd.DataFrame]:
      """
      Convert p-value(s) to significance stars.

      Example
      -------
      >>> p2stars(0.0005)
      '***'
      >>> p2stars("0.03")
      '*'
      >>> p2stars("1e-4")
      '***'
      >>> df = pd.DataFrame({'p_value': [0.001, "0.03", 0.1, "NA"]})
      >>> p2stars(df)
         p_value
      0    0.001 ***
      1    0.030   *
      2    0.100
      3       NA  NA

      Parameters
      ----------
      input_data : float, str, or pd.DataFrame
          The p-value or DataFrame containing p-values to convert.
          For DataFrame, columns matching re.search(r'p[_.-]?val', col.lower()) are considered.
      ns : bool, optional
          Whether to return 'n.s.' for non-significant results (default is False)

      Returns
      -------
      str or pd.DataFrame
          Significance stars or DataFrame with added stars column
      """
      if isinstance(input_data, (float, int, str)):
          return _p2stars_str(input_data, ns)
      elif isinstance(input_data, pd.DataFrame):
          return _p2stars_pd(input_data, ns)
      else:
          raise ValueError("Input must be a float, string, or a pandas DataFrame")
  ```

- For multiple comparisons, please use the FDR correction with `mngs.stats.fdr_correction`:
  - # mngs.stats.fdr_correctiondef
  ``` python
  fdr_correction(results: pd.DataFrame) -> pd.DataFrame:
      if "p_value" not in results.columns:
          return results
      _, fdr_corrected_pvals = fdrcorrection(results["p_value"])
      results["p_value_fdr"] = fdr_corrected_pvals
      results["stars_fdr"] = results["fdr_p_value"].apply(mngs.stats.p2stars)
      return results
  ```

- Statistical values should be rounded by factor 3 and converted in the .3f format (like 0.001) in float.
  - In this purpose, you can utilize `mngs.pd.round` function:
  ``` python
  # mngs.pd.round
  def round(df: pd.DataFrame, factor: int = 3) -> pd.DataFrame:
      def custom_round(column):
          try:
              numeric_column = pd.to_numeric(column, errors='raise')
              if np.issubdtype(numeric_column.dtype, np.integer):
                  return numeric_column
              return numeric_column.apply(lambda value: float(f'{value:.{factor}g}'))
          except (ValueError, TypeError):
              return column

      return df.apply(custom_round)
  ```
- Statistical values must be written in italic font (e.g., \textit{n}).

- Random seed must be fixed as 42.

- Always use `argparse`
  - Use argparse Even when no arguments are necessary
  - Thus, a python file should have at least one argument: -h|--help

- Always use `main` guard:
  ```python
  if __name__ == "__main__":
      main()
  ```

- Adopt modular approaches
  - Smaller functions will increase readability and maintainability

- Naming rules:
  - Variable names in scripts:
    - lpath(s)
    - ldir
    - spath(s)
    - sdir
    - path(s)
    - fname

- Predefined parameters must be written in large latter
  - PARAM

- Implement Python logging
  - Use Python's built-in logging module
    ```python
    import logging
    logging.error()
    logging.warning() 
    logging.info()
    logging.debug()
    ```
  - Replace print statements
    - `print()` -> `logging.info()`
  - Progress tracking
    - `from tqdm import tqdm`
    - `progress_bar = tqdm(total=100)`
  - Debug tracing
    - `from icecream import ic`
    - `ic()` for variable inspection


# Python Rules using my custom MNGS toolbox

- For python scripts, ensure to follow this MNGS FORMAT:
  ``` python
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

  (Remove me: Please fill docstrings above, while keeping the bulette point style, and remove this instruction line)
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
      # parser.add_argument(
      #     "--var",
      #     "-v",
      #     type=int,
      #     choices=None,
      #     default=1,
      #     help="(default: %(default)s)",
      # )
      # parser.add_argument(
      #     "--flag",
      #     "-f",
      #     action="store_true",
      #     default=False,
      #     help="(default: %%(default)s)",
      # )
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

- Always use `argparse`
  - Use argparse Even when no arguments are necessary
  - Thus, a python file should have at least one argument: -h|--help

- Docstrings should be writte in the NumPy style:
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
      ...
  ```
- Take modular approaches
  - Smaller functions will increase readability and maintainability

- Naming rules are:
  - lpath(s)/spath(s) for path(s) to load/save

- Use my custom python utility package, `mngs` (monogusa; meaning lazy person in Japanese). 
  - Especially, use 
    - `mngs.gen.start(...)` (fixme; it might be better for me to handle this automatically using hook)
    - `mngs.gen.close(...)` (fixme; it might be better for me to handle this automatically using hook)
    - `mngs.io.load_configs()`
      - Load YAML files under ./config and concatenate as a dot-accesible dictionary
      - Centralize variables here
        - e.g., paths to ./config/PATH.yaml
        - e.g., mnist-related parameters to ./config/MNIST.yaml
    - `mngs.io.load()`
      - Ensure to use relative path from the project root
      - Ensure to load data from (symlinks of) `./data` directory, instead of from `./scripts`
      - Use CONFIG.PATH.... to load data
    - `mngs.io.save(obj, spath, symlink_from_cwd=True)`
      - From the extension of spath, saving code will be handled automatically
      - Note that save path must be relative to use symlink_from_cwd=True
        - Especially, this combination is expected because this organize data (and symlinks) under the ./data directory: `mngs.io.save(obj, ./data/path/to/data.ext, symlink_from_cwd=True)`
    - `mngs.plt.subplots(ncols=...)`
      - Use CONFIG.PATH.... to save data
      - This is a matplotlib.plt wrapper. 
      - Plotted data will be saved in the csv with the same name of the figure
      - CSV file will be the same format expected in a plotting software, SigmaPlot
    - `mngs.str.printc(message, c='blue)`
      - Acceptable colors: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', or 'grey' 
        - (default is None, which means no color)

- If errors or issues found in previous rounds, fix them

- Directory names should be noun forms:
    - e.g., mnist-creation/, mnist-classification/

- Script file name should:
  - Start from verb if the script expects inputs and produce outputs
  - Definition files for classes should be Capital:
    - ClassName.py

# Programming Python Stats Rules
    - Statistical results must be reported with p value, stars (explained later), sample size or dof, effect size, test name, statistic, and null hypothes as much as possible.
      ```python
      results = {
           "p_value": pval,
           "stars": mngs.stats.p2stars(pval),
           "n1": n1,
           "n2": n2,
           "dof": dof,
           "effsize": effect_size,
           "test_name": test_name_text,
           "statistic": statistic_value,
           "H0": null_hypothes_text,
      }
      ```
      - So, if you want to use scipy.stats package, do not forget to calculate necessary values listed above.

    - P-values should be output with stars using mngs.stats.p2stars:
      ```python
      # mngs.stats.p2stars
      def p2stars(input_data: Union[float, str, pd.DataFrame], ns: bool = False) -> Union[str, pd.DataFrame]:
          """
          Convert p-value(s) to significance stars.

          Example
          -------
          >>> p2stars(0.0005)
          '  -  -  -'
          >>> p2stars("0.03")
          '  -'
          >>> p2stars("1e-4")
          '  -  -  -'
          >>> df = pd.DataFrame({'p_value': [0.001, "0.03", 0.1, "NA"]})
          >>> p2stars(df)
             p_value
          0    0.001   -  -  -
          1    0.030     -
          2    0.100
          3       NA  NA

          Parameters
          ----------
          input_data : float, str, or pd.DataFrame
              The p-value or DataFrame containing p-values to convert.
              For DataFrame, columns matching re.search(r'p[_.-]?val', col.lower()) are considered.
          ns : bool, optional
              Whether to return 'n.s.' for non-significant results (default is False)

          Returns
          -------
          str or pd.DataFrame
              Significance stars or DataFrame with added stars column
          """
          if isinstance(input_data, (float, int, str)):
              return _p2stars_str(input_data, ns)
          elif isinstance(input_data, pd.DataFrame):
              return _p2stars_pd(input_data, ns)
          else:
              raise ValueError("Input must be a float, string, or a pandas DataFrame")
      ```

    - For multiple comparisons, please use the FDR correction with `mngs.stats.fdr_correction`:
      - # mngs.stats.fdr_correctiondef
      ```python
      fdr_correction(results: pd.DataFrame) -> pd.DataFrame:
          if "p_value" not in results.columns:
              return results
          _, fdr_corrected_pvals = fdrcorrection(results["p_value"])
          results["p_value_fdr"] = fdr_corrected_pvals
          results["stars_fdr"] = results["fdr_p_value"].apply(mngs.stats.p2stars)
          return results
      ```

    - Statistical values should be rounded by factor 3 and converted in the .3f format (like 0.001) in float.
      - In this purpose, you can utilize `mngs.pd.round` function:
      ```python
      # mngs.pd.round
      def round(df: pd.DataFrame, factor: int = 3) -> pd.DataFrame:
          def custom_round(column):
              try:
                  numeric_column = pd.to_numeric(column, errors='raise')
                  if np.issubdtype(numeric_column.dtype, np.integer):
                      return numeric_column
                  return numeric_column.apply(lambda value: float(f'{value:.{factor}g}'))
              except (ValueError, TypeError):
                  return column

          return df.apply(custom_round)
      ```
    - Statistical values must be written in italic font (e.g., \textit{n}).

    - Random seed must be fixed as 42.


## Programming Shell Scripts Rules

- Include one-line explanation for function, followed by example usage at the first lines of a function.
- Please ensure if-fi syntaxes are correct.
- A complete shell script MUST INCLUDE:
  - argument parser and usage (with -h|--help option)
  - logging functionality


- The template of shell script is as follows:
  ``` bash
  #!/bin/bash
  # script-name.sh
  # Author: ywatanabe (ywatanabe@alumni.u-tokyo.ac.jp)
  # Date: $(date +"%Y-%m-%d-%H-%M")

  LOG_FILE=".$0.log" # Do not remove existing extension (e.g., script.sh.log is preferred)

  usage() {
      echo "Usage: $0 [-s|--subject <subject>] [-m|--message <message>] [-h|--help]"
      echo-
      echo "Options:"
      echo "  -s, --subject   Subject of the notification (default: 'Subject')"
      echo "  -m, --message   Message body of the notification (default: 'Message')"
      echo "  -h, --help      Display this help message"
      echo
      echo "Example:"
      echo "  $0 -s "About the Project A" -m "Hi, ..."
      echo "  $0 -s "Notification" -m "This is a notification from ..."
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

## RUN ALL FORMAT
  - For run_all.sh, please write a sequence of calls from the project root directory
# Format: 
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

## For slurm

# Programming Sorting Rules

- Functions must be sorted considering their hierarchy.
- Upstream functions should be placed in upper positions
  - from top (upstream functions) to down (utility functions)
- Do not change any code contents during sorting
- Includes comments to show hierarchy

- Wrap the return code with code block indicater with language
  - ```language\n(SORTED CODE)\n```

- Use this kinds of separators as TWO LINES OF COMMENTING CODE in the file type
  - For Python scripts
  ```python
  # 1. Main entry point
  # ---------------------------------------- 


  # 2. Core functions
  # ---------------------------------------- 


  # 3. Helper functions
  # ---------------------------------------- 
  ```
  - For Elisp scripts
  ```elisp
  ;; 1. Main entry point
  ;; ---------------------------------------- 


  ;; 2. Core functions
  ;; ---------------------------------------- 


  ;; 3. Helper functions
  ;; ---------------------------------------- 
  ```
  - For Shell scripts
  ```shell
  # 1. Main entry point
  # ---------------------------------------- 


  # 2. Core functions
  # ---------------------------------------- 


  # 3. Helper functions
  # ---------------------------------------- 
  ```

  - Heading titles can be edited flexibly
  - But keep the separating lines


## Programming General Rules
- Determine which language I am requesting to process.
	- I frequently use Python, Elisp, shell script, LaTeX, HTML, CSS, JavaScript, and others.
	- If you cannot identify a specific language, please provide several versions in potential languages.
    - If I ask you same kinds of code multiple times, I might be confused. In that case, please consider adding debugging lines (like printing, logging, or error handling) in a minimum manner.
    - If you need further source, please respond like this: "Please provide me "<SCRIPT-NAME>, <FUCNTION_NAME>, <ETCETRA>".

- Avoid unnecessary comments as they are disruptive.
	- Return only the updated code without comments.

- Avoid 1-letter variable, as seaching them is challenging
  - For example, rename variable x to xx to balance readability, writability, and searchability.

- Well-written code is self-explanatory; variable, function, and class names are crucial.
	- Ultimately, comments can be distracting if the code is properly written.

- Subjects of commenting sentences should be "this file/code/function/and so on" implicitly; thus, verbs should be in their singular form (such as "# Computes ..." instead of "# Compute ...").

- Docstring with example usage is necessary.

- Do not care about the length of your output. If you cannot output all of your revision, I will ask you "continue" in the next interaction.

- Do not change headers (such as time stamp, file name, authors) and footers of the code (like #EOF).

- Please keep indents (especially at the starting indent of each line). I will insert your revision to my code as is.

- Code should be always provided with code block indicators with triplets and a space (e.g., "``` python\n(CODEHERE)\n```")
  - You might want to use "``` pseudo-code\n(CODEHERE)\n```" or "``` plaintext\n(CODEHERE)\n```" when language is not determined.

#### For Python Code
In test codes:
  - DO NOT USE UNITTEST
  - USE PYTEST
  - Prepare pytest.ini
  - Structure
    - ./src/project-name/__init__.py
    - ./tests/project-name/...
  - Each test function should be smallest
  - Each test file contain only one test function
  - Each Test Class should be defined in a dedicated script
  - Test codes MUST BE MEANINGFUL
  - Implement run_tests.sh (or run_tests.ps1 for projects which only works on Windows) in project root

- Do not change the header of python files:
  ``` python
  #!/usr/bin/env python3
  # -*- coding: utf-8 -*-
  # Time-stamp: \"%s (%s)\"
  # %s

- Update top-level docstring in python files to provide a overview, considering the contents of the file contents. When you don't understand meanings of variables, please ask me simple questions in the first iteration. I will respond to your question and please retry the revision again. This top-level docstring should follow this template, instead of the NumPy style:
  ``` python
  """
  1. Functionality:
     - (e.g., Executes XYZ operation)
  2. Input:
     - (e.g., Required data for XYZ)
  3. Output:
     - (e.g., Results of XYZ operation)
  4. Prerequisites:
     - (e.g., Necessary dependencies for XYZ)

  (Remove me: Please fill docstrings above, while keeping the bulette point style, and remove this instruction line)
  """
  ```

- On the other hand, docstrings for functions and classes should be writte in the NumPy style:
  ``` python
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

- Do not change these commenting lines in python scripts:
  - """Imports"""
  - """Parameters"""
  - """Functions & Classes"""

- Do not skip any lines as much as possible. I am really suprized by your speed and accuracy of coding and appreciate your support and patience.

- My code may include my own Python utility package, mngs. Keep its syntax unchanged.

- When possible, independently implement reusable functions or classes as I will incorporate them into my mngs toolbox.

- Do not forget explicitly define variable types in functions and classes.
  - Use these types and more:
    ``` python
    from typing import Union, Tuple, List, Dict, Any, Optional, Callable
    from collections.abc import Iterable
    ArrayLike = Union[List, Tuple, np.ndarray, pd.Series, pd.DataFrame, xr.DataArray, torch.Tensor]
    ```
- Implement error handling thoroughly.

- Rename variables if your revision makes it better.

- Keep importing packages MECE (Mutually Exclusive and Collectively Exhaustive). Remove/add unnecessary/necessary packages, respectively.

- In code, integer numbers should be written with an underscore every three digits (e.g., 100_000).
- Integer numbers should be shown (in printing, general text, and output data as csv) with an comma every three digits (e.g., 100,000).

- Use modular approaches for reusability, readability, and maintainability. If functions can be split int subroutines or meaningful chunks, do not hesitate to split into pieces, as much as possible.

#### Statistics Rules

- Statistical results must be reported with p value, stars (explained later), sample size or dof, effect size, test name, statistic, and null hypothes as much as possible.
  ``` python
  results = {
       "p_value": pval,
       "stars": mngs.stats.p2stars(pval),
       "n1": n1,
       "n2": n2,
       "dof": dof,
       "effsize": effect_size,
       "test_name": test_name_text,
       "statistic": statistic_value,
       "H0": null_hypothes_text,
  }
  ```
  - So, if you want to use scipy.stats package, do not forget to calculate necessary values listed above.

- P-values should be output with stars using mngs.stats.p2stars:
  ``` python
  # mngs.stats.p2stars
  def p2stars(input_data: Union[float, str, pd.DataFrame], ns: bool = False) -> Union[str, pd.DataFrame]:
      """
      Convert p-value(s) to significance stars.

      Example
      -------
      >>> p2stars(0.0005)
      '***'
      >>> p2stars("0.03")
      '*'
      >>> p2stars("1e-4")
      '***'
      >>> df = pd.DataFrame({'p_value': [0.001, "0.03", 0.1, "NA"]})
      >>> p2stars(df)
         p_value
      0    0.001 ***
      1    0.030   *
      2    0.100
      3       NA  NA

      Parameters
      ----------
      input_data : float, str, or pd.DataFrame
          The p-value or DataFrame containing p-values to convert.
          For DataFrame, columns matching re.search(r'p[_.-]?val', col.lower()) are considered.
      ns : bool, optional
          Whether to return 'n.s.' for non-significant results (default is False)

      Returns
      -------
      str or pd.DataFrame
          Significance stars or DataFrame with added stars column
      """
      if isinstance(input_data, (float, int, str)):
          return _p2stars_str(input_data, ns)
      elif isinstance(input_data, pd.DataFrame):
          return _p2stars_pd(input_data, ns)
      else:
          raise ValueError("Input must be a float, string, or a pandas DataFrame")
  ```

- For multiple comparisons, please use the FDR correction with `mngs.stats.fdr_correction`:
  - # mngs.stats.fdr_correctiondef
  ``` python
  fdr_correction(results: pd.DataFrame) -> pd.DataFrame:
      if "p_value" not in results.columns:
          return results
      _, fdr_corrected_pvals = fdrcorrection(results["p_value"])
      results["p_value_fdr"] = fdr_corrected_pvals
      results["stars_fdr"] = results["fdr_p_value"].apply(mngs.stats.p2stars)
      return results
  ```

- Statistical values should be rounded by factor 3 and converted in the .3f format (like 0.001) in float.
  - In this purpose, you can utilize `mngs.pd.round` function:
  ``` python
  # mngs.pd.round
  def round(df: pd.DataFrame, factor: int = 3) -> pd.DataFrame:
      def custom_round(column):
          try:
              numeric_column = pd.to_numeric(column, errors='raise')
              if np.issubdtype(numeric_column.dtype, np.integer):
                  return numeric_column
              return numeric_column.apply(lambda value: float(f'{value:.{factor}g}'))
          except (ValueError, TypeError):
              return column

      return df.apply(custom_round)
  ```
- Statistical values must be written in italic font (e.g., \textit{n}).

- Random seed must be fixed as 42.

#### For Shell script

- Include one-line explanation for function, followed by example usage at the first lines of a function.
- A complete shell script should include the following components:
  - argument parser and usage (with -h|--help option)
  - logging functionality

- The template of shell script is as follows:
  ``` bash
  #!/bin/bash
  # script-name.sh
  # Author: ywatanabe (ywatanabe@alumni.u-tokyo.ac.jp)
  # Date: $(date +"%Y-%m-%d-%H-%M")

  LOG_FILE=".$0.log"

  usage() {
      echo "Usage: $0 [-s|--subject <subject>] [-m|--message <message>] [-h|--help]"
      echo-
      echo "Options:"
      echo "  -s, --subject   Subject of the notification (default: 'Subject')"
      echo "  -m, --message   Message body of the notification (default: 'Message')"
      echo "  -h, --help      Display this help message"
      echo
      echo "Example:"
      echo "  $0 -s "About the Project A" -m "Hi, ..."
      echo "  $0 -s "Notification" -m "This is a notification from ..."
      exit 1
  }

  my-echo() {
    # Print the arguments with my signature
    #
    # Usage
    # my-echo Hello # Hello (Yusuke Watanabe)

    echo "$@" "(Yusuke Watanabe)"
  }

  main() {
      my-echo "$@"
  }

  main "$@" 2>&1 | tee "$LOG_FILE"

  notify -s "$0 finished" -m "$0 finished"

  # EOF
  ```


#### For Elisp Code

In test codes:
  - Test codes will be executed after loading all environments and in the run time environment
    - Therefore, do not change variables for testing purposes
    - I would like to just check whether codes are working in the variables defined in my run time code
      - DO NOT SETQ/DEFVAR/DEFCUSTOM ANYTHING
      - DO NOT LET/LET* TEST VARIABLES
      - DO NOT LOAD ANYTHING
      - If source scripts are provided, please create the corresponding test files in a one-by-one manner, adding test- prefix to the soruce scripts filenames
      - Split test code into smallest blocks
        - Each ert-deftest should include only one should or should-not
    - Test codes MUST BE MEANINGFUL

  - To check if require statement is valid, use this format IN A ENTRY FILE: loadable tests should not be split across files but concentrate on central entry files.
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
   - Ensure the codes identical between before and after testing; implement cleanup process. DO NOT ALLOW CHANGE DUE TO TEST.
   - When edition is required for testing, first store original information and revert in the cleanup stage.

----------
Now, my input is as follows:
----------
PLACEHOLDER

<!-- EOF --><!-- ---
!-- Timestamp: 2025-05-08 13:13:57
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.emacs.d/lisp/emacs-claude-code/.claude/commands/programming-workflow.md
!-- --- -->

<!-- EOF --><!-- ---
!-- Timestamp: 2025-05-08 14:23:04
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.emacs.d/lisp/emacs-claude-code/.claude/commands/programming-workflow.md
!-- --- -->

## Test-Driven Development (TDD) Workflow

## Test-Driven Development (TDD) Workflow

1. Start with tests
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
     - The quality of test is the quolity of the project
   - Test code should have the expected directory structure in the language and project goals
     - See the detailed rules, formats, and examples in other markdown instructions

2. Verify test failure
   - Run the tests to confirm they fail first
     - Our aim is now clear; all we need is to solve the failed tests
   - Not to write implementation code yet

3. Git commit test files
   - Review the tests for completeness to satisfy the project goals and requirements
     - Not determine the qualities of test files based on source files
       - Prioritize test code over source code
       - Thus, test code MUST BE SOLID
   - Commit the tests when satisfied

4. Implement functionality
   - If the above steps 1-3 completed, now you are allowed to implement source code that passes the tests
   - !!! IMPORTANT !!! NOT TO MODIFY THE TEST FILES IN THIS STEP
   - Iterate until all tests pass

5. Verify implementation quality
   - Use independent subagents to check if implementation overfits to tests
   - Ensure solution meets broader requirements beyond tests

6. Summarize the current iteration by listing:
   -  What were verified
   -  What are not verified yet
      -  Reasons why they are not verified if not expected

7. Commit implementation
   - Commit the source code once satisfied

## Project Management Progress Rules

- Direction of the project is managed under `./project_management`:
  - `./project_management/progress.md`
    - Main progress management file. You should update this as project advances.
    - Use tags:
      - TODO
        - Format: [ ] contents
        - For contents that need to be addressed or completed.
      - DONE
        - Format: [x] contents
        - Fill checkbox
        - For contents that have been completed (considered as done by agents).
      - JUSTIFICATION
        - Format: __justification__ | contents
        - References to justify why you determine the contents are DONE
      - ACCEPTED: 
        - Format: __accepted__ | contents
        - For contents accepted by the user.
        - Note: Only users can add or remove this tag.
      - REJECTED:
        - Format: ~~contents~~
        - For contents rejected by the user.
        - Note: Only users can add or remove this tag.
      - SUGGESTION
        - Format: __suggestions__ | contents
        - For contents suggested by agents.

  - `./project_management/progress.mmd`
    - Mermaid diagram definition reflecting the current progress (`./project_management/progress.md`)
    - Use tags as well:

  - `./project_management/progress.svg`
    - SVG file created from the mermaid file

  - `./project_management/progress.gif`
    - GIF image created from the SVG file

  - `./project_management/ORIGINAL_PLAN.md`
    - Original plan created by the user
    - DO NOT EDIT THIS FILE

## Task 2. Understand the formats below:
================================================================================

## ./config Format

```yaml
PATH:
  MAT:
    f"./data/mat/Patient_{patient_id}/Data_{year}_{month}_{day}/Hour_{hour}/UTC_{hour}_{minute}_00.mat"
  MAT_LIST:
    f"./data/mat_list/Patient_{patient_id}_mat_files_list.txt"
    
  DB:
    ECOG:
      f"./data/db/ecog/Patient_{patient_id}.db"
    ECOG1:
      f"./data/db1/ecog/Patient_{patient_id}.db"
    ECOG2:
      f"./data/db2/ecog/Patient_{patient_id}.db"
```

## Python MNGS Format

  - We will call the following format as `mngs format`
    - Ensure to use the `run_main()` function
      - This is quite important that in the mngs project, this handles:
        - stdout/stderr direction, logging, configuration saving, arguments saving, and so on
  - Implement functions and classes under the """Functions & Classes""" tag
  - Combine functions and classes in the main function and call it from run_main() function

```python
#!/usr/bin/env python3
# -  -- coding: utf-8 -  --
# Time-stamp: "2024-11-03 10:33:13 (ywatanabe)"
# File: ./scripts/YYYY-MMDD-hhmmss-<title>/NNN_filename.py

__file__ = "./scripts/YYYY-MMDD-hhmmss-<title>/NNN_filename.py"

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

(Remove me: Please fill docstrings above, while keeping the bulette point style, and remove this instruction line)
"""

"""Imports"""
import os
import sys
import argparse
import mngs

"""Warnings"""
# mngs.pd.ignore_SettingWithCopyWarning()
# warnings.simplefilter("ignore", UserWarning)
# with warnings.catch_warnings():
#     warnings.simplefilter("ignore", UserWarning)

"""Parameters"""
# from mngs.io import load_configs
# CONFIG = load_configs()

"""Functions & Classes"""
def function1(arg1, arg2, ...):
    return ...

def function2(arg1, arg2, ...):
    return ...
    
def main(args):
    out1 = function1(args.xxx)
    out2 = function2(args.xxx, out1)
    mngs.io.save(out1, "./data/example/output.npy", from_cwd=True)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    import mngs
    script_mode = mngs.gen.is_script()
    parser = argparse.ArgumentParser(description='')
    # parser.add_argument(
    #     "--var",
    #     "-v",
    #     type=int,
    #     choices=None,
    #     default=1,
    #     help="(default: %(default)s)",
    # )
    # parser.add_argument(
    #     "--flag",
    #     "-f",
    #     action="store_true",
    #     default=False,
    #     help="(default: %%(default)s)",
    # )
    args = parser.parse_args()
    mngs.str.printc(args, c='yellow')
    return args

# Always use this function without any modification
def run_main() -> None:
    """Initialize mngs framework, run main function, and cleanup."""
    global CONFIG, CC, sys, plt

    import sys
    import matplotlib.pyplot as plt
    import mngs

    args = parse_args()

    # Start mngs framework
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(
        sys,
        plt,
        args=args,
        file=__file__,
        sdir_suffix=None,
        verbose=False,
        agg=True,
    )

    # Main
    exit_status = main(args)

    # Close the mngs framework
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

## Python Docstring Format
  - Docstring must follow this format:
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

## Python Script MNGS Format

!!! IMPORTANT !!!
ENSURE TO USE THIS MNGS FORMAT FOR ANY PYTHON SCRIPT FILE.
- ENSURE TO IMPLEMENT `main()` and WRAP IT WITH THE `run_main()` FUNCTION
- THE `run_main()` FUNCTION MUST BE IDENTICAL WITHOUT ANY LETTER MODIFIED
  - This is quite important that in the mngs project, this handles:
    - configuration
    - seeds fixation
    - stdout/stderr handling
    - logging
    - saving directory handling
    - symbolic link handling
    - arguments saving
    - and more
- Combine functions and classes in the main function and call it from run_main() function

=== PYTHON MNGS TEMPLATE STARTS ===
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

(Remove me: Please fill docstrings above, while keeping the bulette point style, and remove this instruction line)
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
def function1(arg1, arg2, ...):
    return ...

def function2(arg1, arg2, ...):
    return ...
    
def main(args):
    out1 = function1(args.xxx)
    out2 = function2(args.xxx, out1)
    mngs.io.save(out1, "./data/example/output.npy", symlink_from_cwd=True)

import argparse
def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    import mngs
    script_mode = mngs.gen.is_script()
    parser = argparse.ArgumentParser(description='')
    # parser.add_argument(
    #     "--var",
    #     "-v",
    #     type=int,
    #     choices=None,
    #     default=1,
    #     help="(default: %(default)s)",
    # )
    # parser.add_argument(
    #     "--flag",
    #     "-f",
    #     action="store_true",
    #     default=False,
    #     help="(default: %%(default)s)",
    # )
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
=== PYTHON MNGS TEMPLATE ENDS ===

## Shell Script Format

```bash
#!/bin/bash
# ~/.bin/demo_backup.sh
# Author: ywatanabe (ywatanabe@alumni.u-tokyo.ac.jp)
# Date: $(date +"%Y-%m-%d-%H-%M")

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
}

{ main "$@"; } 2>&1 | tee "$LOG_FILE"
```


## Elisp Format
```bash
# YOUR PYTHON CODE
```
``` org
#+TITLE: Emacs Claude Code - Project Progress Report
#+AUTHOR: ywatanabe
#+DATE: 2025-05-08 17:35:22
#+FILE: /home/ywatanabe/.dotfiles/.emacs.d/lisp/emacs-claude-code/.claude/commands/formats/completed-project-management-progress.md

* Title

| Type | Stat | Description                                        | User |
|------|------|----------------------------------------------------|------|
| 🚀 T | [x]  | Emacs Claude Code - Streamlined Claude AI Interface | 👍 A |

* Goals, Milestones, and Tasks

** 🎯 Goal 1: Create a modular buffer management system for Claude integration

| Type | Stat | Description                                    | User |
|------|------|------------------------------------------------|------|
| 🎯 G | [x]  | Buffer management system                       | 👍 A |
|------|------|------------------------------------------------|------|
| 🏁 M | [x]  | Buffer registry functionality                  | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Create buffer registration system              | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-registry.el`        | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Implement current buffer tracking              | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-current.el`         | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Build stale buffer detection and cleanup       | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-stale.el`           | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Create buffer state management                 | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-state.el`           | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Implement buffer timestamp tracking            | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-timestamp.el`       | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Add buffer navigation capabilities             | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer-navigation.el`      | 👍 A |
|------|------|------------------------------------------------|------|
| 📋 T | [x]  | Create umbrella module with full test coverage | 👍 A |
|      | [x]  | 📌 `/ecc-buffer/ecc-buffer.el`                 | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer.el`                 | 👍 A |

** 🎯 Goal 2: Implement Claude state detection and response system

| Type | Stat | Description                                 | User |
|------|------|---------------------------------------------|------|
| 🎯 G | [x]  | Claude state detection and response system  | 👍 A |
|------|------|---------------------------------------------|------|
| 🏁 M | [x]  | Claude state detection                      | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Detect waiting state                        | 👍 A |
|      | [x]  | 📌 `/ecc-state-detect.el`                   | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Detect Y/N prompt state                     | 👍 A |
|      | [x]  | 📌 `/ecc-state.el`                          | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Detect Y/Y/N prompt state                   | 👍 A |
|------|------|---------------------------------------------|------|
| 🏁 M | [x]  | Auto-response system                        | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Implement auto-accept for prompts           | 👍 A |
|      | [x]  | 📌 `/ecc-auto.el`                           | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Create notification system for auto-accepts | 👍 A |

** 🎯 Goal 3: Create template system for efficient Claude interactions

| Type | Stat | Description                                 | User |
|------|------|---------------------------------------------|------|
| 🎯 G | [x]  | Template system for Claude interactions     | 👍 A |
|------|------|---------------------------------------------|------|
| 🏁 M | [x]  | Template loading and management             | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Template file loading                       | 👍 A |
|      | [x]  | 📌 `/ecc-templates.el`                      | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Template caching                            | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Template directory management               | 👍 A |
|------|------|---------------------------------------------|------|
| 🏁 M | [x]  | Default templates                           | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Programming template                        | 👍 A |
|      | [x]  | 📌 `/templates/claude/Programming.md`       | 👍 A |
|------|------|---------------------------------------------|------|
| 📋 T | [x]  | Create additional template files            | 👍 A |
|      | [x]  | 📌 `/templates/claude/*`                    | 👍 A |

** 🎯 Goal 4: Implement user interaction features

| Type | Stat | Description                               | User |
|------|------|-------------------------------------------|------|
| 🎯 G | [x]  | User interaction functions and keybindings | 👍 A |
|------|------|-------------------------------------------|------|
| 🏁 M | [x]  | Region and buffer processing              | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Send region to Claude                     | 👍 A |
|      | [x]  | 📌 `/ecc-send.el`                         | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Send buffer to Claude                     | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Send template to Claude                   | 👍 A |
|------|------|-------------------------------------------|------|
| 🏁 M | [x]  | Keybinding system                         | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Create prefix map                         | 👍 A |
|      | [x]  | 📌 `/ecc-bindings.el`                     | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Assign commands to key combinations       | 👍 A |
|------|------|-------------------------------------------|------|
| 📋 T | [x]  | Make keybindings customizable             | 👍 A |

** 🎯 Goal 5: Build test infrastructure

| Type | Stat | Description                                | User |
|------|------|------------------------------------------|------|
| 🎯 G | [x]  | Test infrastructure and coverage          | 👍 A |
|------|------|------------------------------------------|------|
| 🏁 M | [x]  | Buffer module tests                      | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Test buffer registry                     | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-registry.el`  | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Test buffer navigation                   | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-navigation.el` | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Test buffer timestamp                    | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-timestamp.el` | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Add missing buffer tests                 | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-current.el`   | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-state.el`     | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-stale.el`     | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-variables.el` | 👍 A |
|      | [x]  | 📌 `/tests/test-ecc-buffer-verification.el` | 👍 A |
|------|------|------------------------------------------|------|
| 🏁 M | [x]  | Test runner                              | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Create test runner script                | 👍 A |
|      | [x]  | 📌 `/run-tests.sh`                       | 👍 A |
|------|------|------------------------------------------|------|
| 📋 T | [x]  | Create mock implementations for testing  | 👍 A |
|      | [x]  | 📌 `/tests/test-mock-vterm.el`           | 👍 A |

** 🎯 Goal 6: Implement additional features and improvements

| Type | Stat | Description                            | User |
|------|------|----------------------------------------|------|
| 🎯 G | [ ]  | Additional features and refinements    | 👀 T |
|------|------|----------------------------------------|------|
| 🏁 M | [ ]  | Repository integration                 | 👀 T |
|------|------|----------------------------------------|------|
| 📋 T | [x]  | Copy repository contents functionality | 👍 A |
|      | [x]  | 📌 `/ecc-repository.el`                | 👍 A |
|------|------|----------------------------------------|------|
| 📋 T | [ ]  | Enhanced repository selection          | 👀 T |
|------|------|----------------------------------------|------|
| 🏁 M | [ ]  | Performance optimizations              | 👀 T |
|------|------|----------------------------------------|------|
| 📋 T | [ ]  | Optimize buffer handling for large files | 👀 T |
|------|------|----------------------------------------|------|
| 📋 T | [ ]  | Improve template caching               | 👀 T |

* Suggestions from Agents

| Type | Stat | Description                                | User |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Enhanced Template Categories              | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Project-specific Context Integration      | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | History Management Improvements           | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Enhanced Buffer Visualization            | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Context Awareness                        | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Client API Integration                   | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Collaborative Features                   | 👀 T |
|------|------|------------------------------------------|------|
| 💡 S | [ ]  | Performance Optimization                 | 👀 T |

* Legend
 
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

# EOF
```


## Progress format

``` org
# +TITLE: Title
# +AUTHOR: ywatanabe
# +DATE: 2025-02-10 14:52:36
# +FILE: path to this file

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
|------|------|---------------------------------------|------|
| 📋 T | [x]  | Not confirmed but completed Task      | 👀 T |
|      | [x]  | 📌 `/path/to/human_readable_file.ext` | 👀 T |
|------|------|---------------------------------------|------|
| ...  |      |                                       |      |


** 🎯 Goal 2: Description

| Type | Stat | Description                           | User |
|------|------|---------------------------------------|------|
| 🎯 G | [ ]  | Goal 2                                | 👍 A |
|------|------|---------------------------------------|------|
| 🏁 M | [x]  | Milestone 1                           | 👍 A |
|------|------|---------------------------------------|------|
| 📋 T | [x]  | Task 1                                | 👍 A |
|      | [x]  | 📌 `/path/to/human_readable_file.ext` | 👍 A |
|------|------|---------------------------------------|------|
| ...  |      |                                       |      |


** 🎯 Goal 3: Description

| Type | Stat | Description             | User |
|------|------|-------------------------|------|
| 🎯 G | [ ]  | Unrealistic Goal 3      | ❌ R |
|------|------|-------------------------|------|
| 🏁 M | [ ]  | Unrealistic Milestone 1 | ❌ R |
|------|------|-------------------------|------|
| 📋 T | [ ]  | Unrealistic Task 1      | ❌ R |
|------|------|-------------------------|------|
| 📋 T | [ ]  | Unrealistic Task 2      | ❌ R |
|------|------|-------------------------|------|
| ...  |      |                         |      |

* Introduction

| Type | Stat | Description  | Direction | User |
|------|------|--------------|-----------|------|
| 🔎 H | [ ]  | Hypothesis 1 | H -> D    | 👍 A |
|------|------|--------------|-----------|------|
| 🔎 H | [ ]  | Hypothesis 2 | D -> H    | 👀 T |
|------|------|--------------|-----------|------|
| ...  |      |              |           |      |

* Methods

** Data

| Type | Stat | Description | User |
|------|------|-------------|------|
| 📊️ D | [x]  | Data 1      | 👍 A |
|------|------|-------------|------|
| 📊 D | [ ]  | Data 2      | ❌ R |
|------|------|-------------|------|
| 📊️ D | [ ]  | Data 3      | 👀 T |
| ...  |      |             |      |

** Tools

| Type | Stat | Description | User |
|------|------|-------------|------|
| 🛠️ T | [x]  | Tool 1      | 👍 A |
|------|------|-------------|------|
| 🛠️ T | [ ]  | Tool 2      | ❌ R |
|------|------|-------------|------|
| 🛠️ T | [ ]  | Tool 3      | 👀 T |
| ...  |      |             |      |


* Suggestions from Agents

| Type | Stat | Description  | User |
|------|------|--------------|------|
| 💡 S | [ ]  | Suggestion 1 | 👀 T |
|------|------|--------------|------|
| 💡 S | [ ]  | Suggestion 2 | 👀 T |
|------|------|--------------|------|
| 💡 S | [ ]  | Suggestion 3 | 👀 T |
| ...  |      |              |      |

* Legend
 
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

# EOF
```
## MNGS Framework Project Structure
My Python utility package, `mngs`, is desined to standardize scientific analyses and applications.
mngs project features predefined directory structure - `./config`, `./data`, `./scripts`

Config:
    - Centralized YAML configuration files (e.g., `./config/PATH.yaml`)
Data:
    - Centralized data files (e.g., `./data/mnist`)

Scripts:
    - Script files (.py and .sh)
    - Directly linked outputs (artifacts and logs)
    - For example, 
        - `./scripts/mnist/plot_images.py` produces:
            - `./scripts/mnist/plot_images_out/data/figures/mnist_digits.jpg`
            - `./scripts/mnist/plot_images_out/RUNNING`
            - `./scripts/mnist/plot_images_out/FINISHED_SUCCESS`
            - `./scripts/mnist/plot_images_out/FINISHED_FAILED`
    - Symlink to `./data` directory can be handled by `mngs.io.save(obj, spath, symlink_from_cwd=True)`
    - Ensure current working directory (`cwd`) is always the project root

To illustrate, this is the format expected for mngs projects:
```plaintext
<project root>
|-- .git
|-- .gitignore
|-- .env
|   `-- bin
|       |-- activate
|       `-- python
|-- config
|   |-- <file_name>.yaml
|   |...
|   `-- <file_name>.yaml
|-- data
|   `-- <dir_name>
|        |-- <file_name>.npy -> ../../scripts/<script_name>/<file_name>.npy (handled by mngs.io.save)
|        |...
|        `-- <file_name>.mat -> ../../scripts/<script_name>/<file_name>.mat (handled by mngs.io.save)
|-- mgmt
|   |-- original_plan.md (DO NOT MODIFY)
|   |-- progress.mmd (Mermaid file for visualization; update this as the project proceed)
|   `-- progress.md (Main progree management file in markdown; update this as the project proceed)
|-- README.md
|-- requirements.txt (for the .env; update this as needed)
`-- scripts
    `-- <dir-name>
        |-- <script_name>.py
        |-- <script_name>
        |    |-- <file_name>.npy
        |    |-- <file_name>.mat
        |    |-- FINISHED_SUCCESS (handled by mngs.io.save)
        |    |    |-- YYYY-MM-DD-hhmmss_<call-id>/(stdout, stderr, and configs)
        |    |    `-- YYYY-MM-DD-hhmmss_<call-id>/(stdout, stderr, and configs)
        |    |-- FINISHED_FAILURE (handled by mngs.io.save)
        |    |    `-- YYYY-MM-DD-hhmmss_<call-id>/(stdout, stderr, and configs)
        |    `-- RUNNING (handled by mngs.io.save)
        |         `-- YYYY-MM-DD-hhmmss_<call-id>/(stdout, stderr, and configs)
        |-- <script_name>.sh 
        `-- <script_name>.sh.log 
```

# Task 3. Understand the examples below
================================================================================

## Example of YAML file under ./config

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

Another example is:

```yaml
# Time-stamp: "2025-01-15 10:14:13 (ywatanabe)"
# File: ./neurovista/config/PATH.yaml

PATH:
  MAT:
    f"./data/mat/Patient_{patient_id}/Data_{year}_{month}_{day}/Hour_{hour}/UTC_{hour}_{minute}_00.mat"
```

## Example of MNGS Python Script

```python
#!/usr/bin/env python3
# -  -- coding: utf-8 -  --
# Time-stamp: "2025-01-18 16:58:19 (ywatanabe)"
# File: ./scripts/2025-0117-061607-mnist/001_download_mnist.py

__file__ = "./scripts/2025-0117-061607-mnist/001_download_mnist.py"

"""
Functionalities:
  - Downloads MNIST dataset using sklearn
  - Preprocesses images and labels
  - Splits into train/test sets
  - Saves numpy arrays

Dependencies:
  - scripts:
    - None
  - packages:
    - numpy
    - sklearn 
    - mngs
IO:
  - input-files:
    - None (downloads from OpenML)
  - output-files:
    - ./data/mnist/train_images.npy : Training images (60000, 28, 28) float32
    - ./data/mnist/train_labels.npy : Training labels (60000,) int64 
    - ./data/mnist/test_images.npy : Test images (10000, 28, 28) float32
    - ./data/mnist/test_labels.npy : Test labels (10000,) int64
"""


"""Imports"""
import argparse
import numpy as np
from sklearn.datasets import fetch_openml
import mngs

"""Parameters"""
CONFIG = mngs.io.load_configs()

"""Functions & Classes"""
def main(args):
    mnist = fetch_openml("mnist_784", version=1, cache=True, as_frame=False)

    X_train, y_train = mnist["data"][:60000], mnist["target"][:60000]
    X_test, y_test = mnist["data"][60000:], mnist["target"][60000:]

    X_train = X_train.reshape(-1, 28, 28).astype(np.float32) / 255.0
    X_test = X_test.reshape(-1, 28, 28).astype(np.float32) / 255.0
    y_train = y_train.astype(np.int64)
    y_test = y_test.astype(np.int64)

    mngs.io.save(X_train, "mnist/train_images.npy", symlink_from_cwd=True)
    mngs.io.save(y_train, "mnist/train_labels.npy", symlink_from_cwd=True)
    mngs.io.save(X_test, "mnist/test_images.npy", symlink_from_cwd=True)
    mngs.io.save(y_test, "mnist/test_labels.npy", symlink_from_cwd=True)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    script_mode = mngs.gen.is_script()
    parser = argparse.ArgumentParser(
        description="Download and save the MNIST dataset."
    )
    args = parser.parse_args()
    mngs.str.printc(args, c="yellow")
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

    args = parse_args()

    # Start mngs framework
    CONFIG, sys.stdout, sys.stderr, plt, CC = mngs.gen.start(
        sys,
        plt,
        args=args,
        file=__file__,
        sdir_suffix=None,
        verbose=False,
        agg=True,
    )

    # Main
    exit_status = main(args)

    # Close the mngs framework
    mngs.gen.close(
        CONFIG,
        verbose=False,
        notify=False,
        message="",
        exit_status=exit_status,
    )


if __name__ == "__main__":
    run_main()

# EOF
```

## Example of Shell Script
```bash
#!/bin/bash
# ~/.bin/echo_steps.sh
# Author: ywatanabe (ywatanabe@alumni.u-tokyo.ac.jp)
# Date: $(date +"%Y-%m-%d-%H-%M")

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

initialize() {
    echo "Step 1: Initialize"
    sleep 1
}

process() {
    echo "Step 2: Process"
    sleep 1
}

complete() {
    echo "Step 3: Complete"
    sleep 1
}

main() {
    while [[ $# -gt 0 ]]; do
        case $1 in
        -h|--help) usage ;;
          -) echo "Unknown option: $1"; usage ;;
        esac
    done

    echo "Starting script execution..."
    initialize
    process 
    complete
    echo "Finished script execution"
}

{ main "$@"; } 2>&1 | tee "$LOG_FILE"
```


## Example of project management

``` org
# +TITLE: MNIST Digit Classification Project
# +AUTHOR: ywatanabe
# +DATE: 2025-02-10 14:52:36
# +FILE: /home/ywatanabe/proj/llemacs/resources/prompts/components/examples/mgmt-progress.org

* Title

| Type | Stat | Description                        | User |
|------|------|------------------------------------|------|
| 🚀 T | [x]  | *mnist digit clf*                  | 👍 A |
|------|------|------------------------------------|------|
| 🚀 T | [ ]  | *MNIST Digit Classification Project* | 👍 A |


* Goals, Milestones, and Tasks

** 🎯 Goal 1: Prepare and Preprocess Data

| Type | Stat | Description                                  | User |
|------|------|----------------------------------------------|------|
| 🎯 G | [ ]  | Prepare and Preprocess Data                  | 👍 A |
|------|------|----------------------------------------------|------|
| 🏁 M | [x]  | Acquire MNIST Dataset                        | 👍 A |
|------|------|----------------------------------------------|------|
| 📋 T | [x]  | Download MNIST training and testing datasets | 👍 A |
|      | [x]  | 📊 ./data/mnist/                             | 👍 A |
|------|------|----------------------------------------------|------|
| 🏁 M | [ ]  | Preprocess and Augment Data                  | 👀 T |
|------|------|----------------------------------------------|------|
| 📋 T | [ ]  | Normalize pixel values                       | 👀 T |
|      | [ ]  | 📌 ./scripts/mnist/normalization.py          | 👀 T |
|------|------|----------------------------------------------|------|
| 📋 T | [ ]  | Reshape and format data for model input      | 👀 T |
|      | [ ]  | 📌 ./scripts/mnist/reshape.py                | 👀 T |
|------|------|----------------------------------------------|------|
| 📋 T | [ ]  | Perform data augmentation techniques         | 👀 T |
|      | [ ]  | 📌 ./scripts/mnist/data_augmentation.py      | 👀 T |

** 🎯 Goal 2: Develop and Train Baseline CNN Model

| Type | Stat | Description                                                    | User |
|------|------|----------------------------------------------------------------|------|
| 🎯 G | [ ]  | Develop and Train Baseline CNN Model                           | 👍 A |
|------|------|----------------------------------------------------------------|------|
| 🏁 M | [x]  | Design CNN architecture                                        | 👍 A |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [x]  | Define the number of layers and filters                        | 👍 A |
|      | [x]  | 📌 Configuration in `./config/cnn_config.yaml`                 | 👍 A |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [x]  | Select activation functions and pooling strategies             | 👍 A |
|      | [x]  | 📌 Details in `./config/cnn_config.yaml`                       | 👍 A |
|------|------|----------------------------------------------------------------|------|
| 🏁 M | [ ]  | Implement the CNN model in code                                | 👀 T |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [ ]  | Code the model using Keras API                                 | 👀 T |
|      | [ ]  | 📌 Code to be written in `./models/cnn_model.py`               | 👀 T |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [ ]  | Compile the model with appropriate optimizer and loss function | 👀 T |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [ ]  | Train the model on preprocessed MNIST training data            | 👀 T |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [ ]  | Set training parameters (epochs, batch size)                   | 👀 T |
|------|------|----------------------------------------------------------------|------|
| 📋 T | [ ]  | Monitor training progress and adjust as necessary              | 👀 T |

** 🎯 Goal 3: Evaluate Model Performance

| Type | Stat | Description                                         | User |
|------|------|-----------------------------------------------------|------|
| 🎯 G | [ ]  | Evaluate Model Performance                          | 👍 A |
|------|------|-----------------------------------------------------|------|
| 🏁 M | [ ]  | Test the model on MNIST testing data                | 👀 T |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Calculate accuracy and loss on test set             | 👀 T |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Generate confusion matrix and classification report | 👀 T |


** 🎯 Goal 4: Improve Model Accuracy and Generalization

| Type | Stat | Description                                             | User |
|------|------|---------------------------------------------------------|------|
| 🎯 G | [ ]  | Improve Model Accuracy and Generalization               | 👍 A |
|------|------|-----------------------------------------------------|------|
| 🏁 M | [ ]  | Apply Additional Data Augmentation Techniques           | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Implement random rotations, shifts, and flips           | 💡 S |
|      | [ ]  | 📌 Enhances model robustness to variations | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Retrain the model with augmented data                   | 💡 S |
|------|------|-----------------------------------------------------|------|
| 🏁 M | [ ]  | Perform Hyperparameter Tuning                           | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Adjust learning rates, batch sizes, and optimizer types | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Use techniques like grid search or random search        | 💡 S |
|------|------|-----------------------------------------------------|------|
| 🏁 M | [ ]  | Implement Regularization Methods                        | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Add dropout layers to prevent overfitting               | 💡 S |
|------|------|-----------------------------------------------------|------|
| 📋 T | [ ]  | Apply L1/L2 regularization to weights                   | 💡 S |

* Introduction

| Type | Stat | Description                                                                                  | User |
|------|------|----------------------------------------------------------------------------------------------|------|
| 🔎 H | [ ]  | Implementing a CNN will achieve over 99% accuracy on MNIST.                                  | 👀 T |
|------|------|----------------------------------------------------------------------------------------------|------|
| 🔎 H | [ ]  | Applying data preprocessing and augmentation will improve model accuracy and generalization. | 👀 T |

* Methods

** Tools

| Type | Stat | Description                                       | User |
|------|------|---------------------------------------------------|------|
| 🛠️ T  | [x]  | Python programming language.                      | 👍 A |
|------|------|---------------------------------------------------|------|
| 🛠️ T  | [x]  | TensorFlow and Keras libraries for deep learning. | 👍 A |
|------|------|---------------------------------------------------|------|
| 🛠️ T  | [ ]  | GPU resources for accelerated training.           | 👀 T |

* Suggestions from Agents

| Type | Stat | Description                                                                                   | User |
|------|------|-----------------------------------------------------------------------------------------------|------|
| 💡 S | [ ]  | Experiment with batch normalization layers to improve training speed and stability.           | 👀 T |
|------|------|-----------------------------------------------------------------------------------------------|------|
| 💡 S | [ ]  | Try deeper network architectures like ResNet or DenseNet for potential accuracy improvements. | 👀 T |
|------|------|-----------------------------------------------------------------------------------------------|------|
| 💡 S | [ ]  | Implement cross-validation to obtain more reliable estimates of model performance.            | 👀 T |

* Legend
 
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
```

## Example of MGNS Framework
fixme;

## Example of Report Org

```org
# Timestamp: "YYYY-MM-DD HH:mm:ss (ywatanabe)"
# File: <path-to-projects>/<project-id>-<project-name>/reports/YYYY-MMDD-HHmmss-<title>-report.org

#+STARTUP: showall
#+OPTIONS: toc:nil num:nil
#+TITLE: <title>
#+DATE: YYYY-MMDD-HHmmss

  - Project Directory
<path-to-projects>/<project-id>-<project-name>/

  - Header 1

  -  - Header 2
description:

#+ATTR_HTML: :width 600px
[[file:/path/to/filename.xxx]]


  - PDF
[[file:<path-to-projects>/<project-id>-<project-name>/reports/YYYY-MMDD-HHmmss-<title>/report.pdf]]
```

<!-- EOF -->