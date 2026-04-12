# /sharingan-report — Generate Report from Last Run

Regenerate the Sharingan report from the most recent test run. Useful after manual fixes to update the report.

## Instructions

1. **Find results**: Look for test results in `tests/sharingan/results.json` or the latest Playwright output.

2. **If no results found**: Tell the user to run `/sharingan-test` first.

3. **Parse results**: Count passed, failed, skipped, and fixed tests. Categorize by type (auth, navigation, form, API, permission, accessibility).

4. **Check for previous report**: If `SHARINGAN_REPORT.md` exists, note what was previously reported to show progress.

5. **Generate report**: Write `SHARINGAN_REPORT.md` with:

```markdown
# Sharingan Report
*Generated: [timestamp]*
*Target: [base_url from playwright config or localhost:3000]*
*Framework: [auto-detect from project files]*

## Discovery
- Routes found: [count from scanning project]
- Forms found: [count]
- Auth-protected routes: [count]

## Test Results
| Category | Tests | Passed | Failed | Fixed | Needs Review |
|----------|-------|--------|--------|-------|-------------|
| ...      | ...   | ...    | ...    | ...   | ...         |

## Bugs Found & Fixed
[List any bugs that were auto-fixed with file, issue, fix description]

## Needs Human Review
[List any tests that couldn't be fixed after 3 attempts]

## Screenshots
[Failure screenshots in tests/sharingan/screenshots/]
```

6. **Print summary**: Show the key stats in the console.
