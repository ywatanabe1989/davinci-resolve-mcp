<!-- ---
!-- Timestamp: 2025-05-11 14:25:41
!-- Author: ywatanabe
!-- File: /home/ywatanabe/.claude/commands/develop.md
!-- --- -->

## Test-Driven Development (TDD) Workflow

1. Check `git status` and `git commit` in logical chunks with comments

2. Create a feature branch called `feature/<verb>-<object>`

3. Start with tests
   - Write tests BEFORE WRITING SOURCE CODE BASED ON EXPECTED INPUT/OUTPUT PAIRS
     - !!! IMPORTANT !!! In TDD, test is prioritized over source code
     - Avoid mock implementations
     - Tests should target functionality that doesn't exist yet
     - By following this principle, development can be progressed in a simpler manner

   - Place test code under `./tests`
     - Define structure of `./tests` based on language conventions and project's characteristics
     - Implement `./run-tests.sh` under the project root to RUN ALL THE TESTS under `./tests`
       - However, add an option to run single test as well
       ```
       -d|--debug     Enable debug output. <- DO NOT USE this unless explicitly requested
       -h|--help      Display this help message"
       -s|--single    Run a single test file"
       ```

4. Verify test failure
   - Run the tests TO CONFIRM THEY FAIL FIRST
   - Not to write implementation code yet

5. Git commit test files
   - Review the tests for completeness
   - Commit the tests when satisfied

6. Implement source code
   - If the steps above completed, now you can progress to write source code that passes the tests
   - Not to modify the test files in this step
   - Iterate steps 3-6 until all tests in the current scope pass

7. Verify implementation quality
   - Use independent subagents to check if implementation overfits to tests
   - Ensure solution meets broader requirements beyond tests

8. Commit implementation
   - Last, if above steps passed, commit the code once satisfied
   - Otherwise, restart from step 3

9. Check project structure regularly using: `tree --gitignore`

<!-- EOF -->