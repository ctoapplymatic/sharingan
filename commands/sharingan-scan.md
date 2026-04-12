# /sharingan-scan — Discover Routes Only

Scan the current project to discover all routes, endpoints, and forms without running any tests.

## Instructions

1. **Detect frameworks**: Read `package.json`, `requirements.txt`, `pyproject.toml`, `manage.py` to identify frameworks (Next.js, React, FastAPI, Express, Django).

2. **Discover routes**:
   - **Next.js**: Scan `src/app/` or `app/` directory. Map `page.tsx` files to routes, `route.ts` to API endpoints, identify `layout.tsx` and `middleware.ts`.
   - **FastAPI**: Scan `.py` files for `@app.get/post/put/delete` decorators.
   - **Express**: Scan `.js/.ts` files for `app.get/post(...)` patterns.
   - **Django**: Scan `urls.py` for `path(...)` patterns.
   - **React**: Scan for `<Route path="...">` in component files.

3. **Catalog findings**:
   - All frontend pages/routes
   - All API endpoints with methods
   - All forms (by detecting `<form>`, `onSubmit`, `handleSubmit`)
   - Auth-protected routes (by detecting auth middleware, `useSession`, `Depends(get_current_user)`)
   - Dynamic routes with parameters

4. **Generate test plan**: For each discovered route, plan what tests would be generated:
   - Auth flow tests for login/signup routes
   - Navigation tests for all page routes
   - Form validation tests for routes with forms
   - API tests for all endpoints
   - Permission tests for auth-protected routes

5. **Output**: Write the plan to `SHARINGAN_PLAN.md` with a structured summary:

```markdown
# Sharingan Test Plan
*Generated: [timestamp]*
*Framework: [detected]*

## Discovered Routes
| Route | Type | Method | Auth | Forms | Source File |
|-------|------|--------|------|-------|-------------|
| /     | page | GET    | No   | No    | src/app/page.tsx |
| ...   | ...  | ...    | ...  | ...   | ...         |

## Planned Tests
| Category | Count | Priority |
|----------|-------|----------|
| Auth     | N     | Critical |
| Navigation | N  | Critical |
| Forms    | N     | High     |
| API      | N     | Critical |
| Permission | N  | Critical |
| Accessibility | N | Medium |
| **Total** | **N** | |
```

This is a dry run — no tests are generated or executed.
