"""Generate test plans from discovered routes."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from sharingan.config import SharinganConfig
from sharingan.discover.base import FrameworkInfo, RouteInfo


class TestCase(BaseModel):
    """A single test case in the plan."""

    name: str = Field(description="Test name (snake_case)")
    route: str = Field(description="Route being tested")
    method: str = Field(default="GET", description="HTTP method")
    category: Literal["auth", "navigation", "form", "api", "permission", "accessibility"] = Field(
        description="Test category"
    )
    priority: Literal["critical", "high", "medium", "low"] = Field(description="Test priority")
    description: str = Field(description="What this test verifies")
    source_file: str = Field(default="", description="Source file for the route under test")


class TestPlan(BaseModel):
    """Complete test plan for a project."""

    project_name: str = Field(default="", description="Name of the project")
    frameworks: list[str] = Field(default_factory=list, description="Detected frameworks")
    auth_tests: list[TestCase] = Field(default_factory=list)
    navigation_tests: list[TestCase] = Field(default_factory=list)
    form_tests: list[TestCase] = Field(default_factory=list)
    api_tests: list[TestCase] = Field(default_factory=list)
    permission_tests: list[TestCase] = Field(default_factory=list)
    accessibility_tests: list[TestCase] = Field(default_factory=list)

    @property
    def total_tests(self) -> int:
        """Total number of test cases."""
        return (
            len(self.auth_tests)
            + len(self.navigation_tests)
            + len(self.form_tests)
            + len(self.api_tests)
            + len(self.permission_tests)
            + len(self.accessibility_tests)
        )

    @property
    def all_tests(self) -> list[TestCase]:
        """All test cases across all categories."""
        return (
            self.auth_tests
            + self.navigation_tests
            + self.form_tests
            + self.api_tests
            + self.permission_tests
            + self.accessibility_tests
        )


def generate_test_plan(frameworks: list[FrameworkInfo], config: SharinganConfig) -> TestPlan:
    """Generate a comprehensive test plan from discovered frameworks.

    Args:
        frameworks: List of detected frameworks with routes.
        config: Sharingan configuration.

    Returns:
        A TestPlan covering all discovered routes.
    """
    plan = TestPlan(
        project_name=config.project_dir.name,
        frameworks=[f.name for f in frameworks],
    )

    for fw in frameworks:
        for route in fw.routes:
            if route.route_type == "layout":
                continue

            if route.route_type == "api":
                _plan_api_tests(plan, route)
            elif route.has_form:
                _plan_form_tests(plan, route)
                _plan_navigation_tests(plan, route)
            else:
                _plan_navigation_tests(plan, route)

            if route.has_auth:
                _plan_permission_tests(plan, route)

        # Add auth flow tests if we found any auth-related routes
        auth_routes = [r for r in fw.routes if r.has_auth or _is_auth_route(r)]
        if auth_routes:
            _plan_auth_flow_tests(plan, auth_routes)

    # Add basic accessibility tests for all page routes
    page_routes = []
    for fw in frameworks:
        page_routes.extend(r for r in fw.routes if r.route_type in ("page", "dynamic"))
    if page_routes:
        _plan_accessibility_tests(plan, page_routes)

    return plan


def _is_auth_route(route: RouteInfo) -> bool:
    """Check if route is an authentication route (login, signup, etc.)."""
    auth_keywords = ["login", "signin", "signup", "register", "auth", "logout", "forgot", "reset"]
    return any(kw in route.path.lower() for kw in auth_keywords)


def _plan_navigation_tests(plan: TestPlan, route: RouteInfo) -> None:
    """Add navigation tests for a route."""
    safe_name = route.path.strip("/").replace("/", "_").replace(":", "") or "home"

    plan.navigation_tests.append(TestCase(
        name=f"{safe_name}_page_loads",
        route=route.path,
        category="navigation",
        priority="critical",
        description=f"Verify {route.path} loads successfully and returns 200",
        source_file=route.source_file,
    ))


def _plan_form_tests(plan: TestPlan, route: RouteInfo) -> None:
    """Add form tests for a route with forms."""
    safe_name = route.path.strip("/").replace("/", "_").replace(":", "") or "home"

    plan.form_tests.append(TestCase(
        name=f"{safe_name}_form_submission",
        route=route.path,
        method="POST",
        category="form",
        priority="high",
        description=f"Verify form on {route.path} submits successfully with valid data",
        source_file=route.source_file,
    ))

    plan.form_tests.append(TestCase(
        name=f"{safe_name}_form_validation",
        route=route.path,
        method="POST",
        category="form",
        priority="high",
        description=f"Verify form on {route.path} shows validation errors for invalid data",
        source_file=route.source_file,
    ))


def _plan_api_tests(plan: TestPlan, route: RouteInfo) -> None:
    """Add API tests for an endpoint."""
    safe_name = route.path.strip("/").replace("/", "_").replace(":", "").replace("{", "").replace("}", "")

    plan.api_tests.append(TestCase(
        name=f"api_{safe_name}_{route.method.lower()}_success",
        route=route.path,
        method=route.method,
        category="api",
        priority="critical",
        description=f"Verify {route.method} {route.path} returns expected response",
        source_file=route.source_file,
    ))

    if route.method in ("POST", "PUT", "PATCH"):
        plan.api_tests.append(TestCase(
            name=f"api_{safe_name}_{route.method.lower()}_invalid_body",
            route=route.path,
            method=route.method,
            category="api",
            priority="high",
            description=f"Verify {route.method} {route.path} returns 422 for invalid request body",
            source_file=route.source_file,
        ))


def _plan_permission_tests(plan: TestPlan, route: RouteInfo) -> None:
    """Add permission/auth-guard tests for protected routes."""
    safe_name = route.path.strip("/").replace("/", "_").replace(":", "") or "home"

    plan.permission_tests.append(TestCase(
        name=f"{safe_name}_requires_auth",
        route=route.path,
        category="permission",
        priority="critical",
        description=f"Verify {route.path} redirects unauthenticated users to login",
        source_file=route.source_file,
    ))


def _plan_auth_flow_tests(plan: TestPlan, auth_routes: list[RouteInfo]) -> None:
    """Add auth flow tests (signup, login, logout)."""
    route_paths = {r.path.lower() for r in auth_routes}

    if any("signup" in p or "register" in p for p in route_paths):
        plan.auth_tests.append(TestCase(
            name="signup_happy_path",
            route="/signup",
            method="POST",
            category="auth",
            priority="critical",
            description="Verify user can sign up with valid credentials",
        ))
        plan.auth_tests.append(TestCase(
            name="signup_existing_email",
            route="/signup",
            method="POST",
            category="auth",
            priority="high",
            description="Verify signup fails for already-registered email",
        ))

    if any("login" in p or "signin" in p for p in route_paths):
        plan.auth_tests.append(TestCase(
            name="login_valid_credentials",
            route="/login",
            method="POST",
            category="auth",
            priority="critical",
            description="Verify user can log in with valid credentials",
        ))
        plan.auth_tests.append(TestCase(
            name="login_invalid_password",
            route="/login",
            method="POST",
            category="auth",
            priority="high",
            description="Verify login fails with invalid password and shows error",
        ))

    plan.auth_tests.append(TestCase(
        name="logout_clears_session",
        route="/",
        category="auth",
        priority="high",
        description="Verify logout clears session and redirects to home/login",
    ))


def _plan_accessibility_tests(plan: TestPlan, page_routes: list[RouteInfo]) -> None:
    """Add basic accessibility tests for pages."""
    for route in page_routes[:5]:  # Limit to first 5 pages
        safe_name = route.path.strip("/").replace("/", "_").replace(":", "") or "home"
        plan.accessibility_tests.append(TestCase(
            name=f"{safe_name}_a11y_basics",
            route=route.path,
            category="accessibility",
            priority="medium",
            description=f"Verify {route.path} has proper heading hierarchy, alt text, and ARIA labels",
            source_file=route.source_file,
        ))
