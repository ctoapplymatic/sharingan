# /sharingan-fix — Diagnose and Fix Failures

Read the last test results and attempt to diagnose and fix all failures. Use this after `/sharingan-test` when you want to fix issues without re-discovering routes.

## Instructions

1. **Read last results**: Look for test results in `tests/sharingan/`. Read the JSON reporter output or the HTML report to identify failing tests.

2. **For each failing test**:

   a. **Read the test code**: Understand what the test expects.

   b. **Read the error**: Parse the error message and stack trace.

   c. **Diagnose**: Determine if this is a:
      - **Test bug**: Wrong selector, timing issue, incorrect expected value
        - Indicators: `locator resolved to 0 elements`, `timeout exceeded waiting for selector`, `strict mode violation`
      - **Application bug**: The app code is actually broken
        - Indicators: `status 500`, `404 Not Found`, `TypeError`, `Unhandled Runtime Error`

   d. **Read source code**: Read the relevant application source file for the route/component/endpoint being tested.

   e. **Fix it**:
      - If test bug → edit the test file
      - If app bug → edit the application source file
      - Safety rules: NEVER modify `.env`, lock files, `node_modules/`, database files, or migrations

   f. **Re-run the fixed test**:
      ```bash
      cd tests/sharingan && npx playwright test --grep "test name" 2>&1
      ```

   g. **Loop**: If still failing, try again (max 3 attempts). After 3 failures, mark as "needs human review".

3. **Report**: Update or create `SHARINGAN_REPORT.md` with:
   - Which tests were fixed
   - What bugs were found and patched
   - Which tests still need human review
   - Before/after for each fix
