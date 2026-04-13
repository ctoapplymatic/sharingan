# /sharingan-resume — Resume After Human Intervention

Resume a paused Sharingan run after the user has resolved a human-in-the-loop situation (email verification, CAPTCHA, OAuth, payment, MFA, etc.).

## Instructions

1. **Check for intervention prompt**: Look for `SHARINGAN_NEEDS_HELP.md` at the project root.
   - If it doesn't exist: no paused run to resume. Tell the user to run `/sharingan` first.
   - If it exists: read it to understand what was stuck.

2. **Check for --skip flag**: If the user ran `/sharingan-resume --skip`, mark the paused test as "skipped (needs human review)" and continue.

3. **Retry the paused test**:
   - Read the paused test name and target URL from `SHARINGAN_NEEDS_HELP.md`.
   - Re-run that specific test:
     ```bash
     cd tests/sharingan && npx playwright test --grep "<test name>"
     ```
   - If it passes: the human fix worked. Delete `SHARINGAN_NEEDS_HELP.md`.
   - If it fails again with the same intervention reason: the human fix didn't stick — ask the user for clarification.
   - If it fails with a different error: diagnose and fix as usual.

4. **Continue the full run**: After resolving the paused test, pick up where Sharingan left off:
   - Run any remaining tests that were queued.
   - Diagnose and fix any new failures.
   - Update `SHARINGAN_REPORT.md` with the final results.

5. **Clean up**: Delete `SHARINGAN_NEEDS_HELP.md` once resolved.

## Safety

- If the intervention was for email verification, check if the test user actually needs a verified email to proceed. Sometimes the app lets you continue without verification — retry and see.
- If the intervention was for payment, confirm the user actually completed a test transaction before retrying.
- Never store credentials from the intervention (verification codes, MFA codes) in any file.
