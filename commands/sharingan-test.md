# /sharingan-test — Generate and Run Tests Only

Discover routes, generate Playwright tests, and run them — but do NOT attempt to fix any failures. Useful for CI/CD pipelines where you want test results without auto-fixes.

## Instructions

1. **Discover**: Follow the same discovery process as `/sharingan` (Step 1) — detect frameworks, scan routes, catalog endpoints and forms.

2. **Generate tests**: Create Playwright test files in `tests/sharingan/` for:
   - Auth flows (signup, login, logout)
   - Navigation (every page loads)
   - Form validation (empty submit, valid submit)
   - API endpoints (correct status codes and response shapes)
   - Permission guards (unauthenticated access blocked)
   - Basic accessibility (headings, alt text, lang)

   Use Playwright best practices: semantic locators, proper waits, isolated tests.

   Create `tests/sharingan/playwright.config.ts` if needed:
   ```typescript
   import { defineConfig } from "@playwright/test";
   export default defineConfig({
     testDir: ".",
     timeout: 30000,
     use: {
       baseURL: "http://localhost:3000",
       screenshot: "only-on-failure",
       trace: "on-first-retry",
     },
   });
   ```

3. **Run tests**:
   ```bash
   cd tests/sharingan && npx playwright test --reporter=json,html 2>&1
   ```

4. **Report results**: Print a summary of:
   - Total tests run
   - Passed / Failed / Skipped
   - List of failing tests with error messages
   - Where to find the full HTML report

Do NOT diagnose or fix failures. Just report what passed and what didn't.
