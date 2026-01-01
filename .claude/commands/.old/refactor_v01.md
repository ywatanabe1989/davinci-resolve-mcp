<!-- ---
!-- Timestamp: 2025-05-11 13:42:01
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/refactor.md
!-- --- -->

## Request
First, unde refactoring guidelines: `~/.claude/docs/programming_guidelines_refactoring.md`
Please refactor the codebase




## Refactoring Rules
1. Commit the current status with appropriate chunks and comments
2. If `feature/refactor` already exits, determine if the current refactoring is in the step or just it is obsolete, already merged branch. In the latter case, please delete the existing `feature/refactor` branch to work on clean environment.
3. If current branch is not `feature/refactor`, create and switch to a new branch called `feature/refactor`.
4. Please try the followings as long as they will improve simplicity, readability, maintainability, while keeping original functionalities.
- Re-organize project structure, standardize names of directories, files, variables, functions, classes/ and so on, move obsolete files under `.old` directory (e.g., `/path/to/obsolete/file.ext` -> `/path/to/obsolete/.old/file.ext`).
5. After refactoring, ensure functionalities are not changed by running tests
6. Once these steps are successfully completed, `git merge` the `feature/refactor` branch into the original branch.


## Script for Renameing
`~/.claude/scripts/replace_and_rename.sh`

``` bash
```

<!-- EOF -->