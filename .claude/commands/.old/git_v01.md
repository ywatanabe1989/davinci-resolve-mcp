<!-- ---
!-- Timestamp: 2025-05-11 14:34:40
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/git_v01.md
!-- --- -->

# Git Command

I would like you to handle version control using git.

## Let me introduce our main workflow:
1. Start from develop branch
2. Checkout to feature branch
3. Confirmed feature branch is correctly implemented in the test-driven development schema
4. Once the feature branch is verified, merge it into develop
5. Push to origin/develop

## Then, my request at the moment is:
1. Check which point where we are now based on `git status`, `git log`, `git stash list`, and so on
2. If conflict found, check if it is minor problems and easily solved or we should work on that later
3. Let me know your opinion, available plans, and reasons in the order of your recommendation
4. Process git commands for the agreed plan
5. Ensure to include the latest test report solely to indicate the reliability of commited/pushed contents.

## Next steps:
- Merge back to develop branch (if current branch is feature branch)
- Push to origin/develop
- Create Pull Request and Auto Merge from origin/develop to origin/main
- Switch to main in local (and pull origin/main?)
- Add tag based on the previous tags conventions
- Add release using the tag with descriptive messages
- Do not forget to switch back to develop branch
- Once merged branches can be deleted if you feel certain

<!-- EOF -->