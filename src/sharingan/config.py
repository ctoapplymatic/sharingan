"""Sharingan configuration management."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class SharinganConfig(BaseModel):
    """Configuration for a Sharingan run."""

    project_dir: Path = Field(default_factory=Path.cwd, description="Root directory of the target project")
    base_url: str = Field(default="http://localhost:3000", description="Base URL of the running application")
    api_base_url: str = Field(default="http://localhost:8000", description="Base URL of the API server")
    test_output_dir: str = Field(default="tests/sharingan", description="Directory for generated test files")
    max_fix_attempts: int = Field(default=3, description="Maximum fix attempts per failing test")
    max_iterations: int = Field(default=5, description="Maximum discover-test-fix loop iterations")
    timeout_ms: int = Field(default=30000, description="Default Playwright timeout in milliseconds")
    screenshot_on_failure: bool = Field(default=True, description="Capture screenshots on test failure")
    headless: bool = Field(default=True, description="Run browser in headless mode")
    browser: Literal["chromium", "firefox", "webkit"] = Field(default="chromium", description="Browser to use for tests")
    report_path: str = Field(default="SHARINGAN_REPORT.md", description="Path for the generated report")
    plan_path: str = Field(default="SHARINGAN_PLAN.md", description="Path for the generated test plan")
    frameworks: list[str] = Field(default_factory=list, description="Detected frameworks (auto-populated)")

    def get_test_output_path(self) -> Path:
        """Return the absolute path for test output."""
        return self.project_dir / self.test_output_dir

    def get_screenshots_path(self) -> Path:
        """Return the absolute path for screenshots."""
        return self.get_test_output_path() / "screenshots"

    def get_report_path(self) -> Path:
        """Return the absolute path for the report."""
        return self.project_dir / self.report_path

    def get_plan_path(self) -> Path:
        """Return the absolute path for the test plan."""
        return self.project_dir / self.plan_path
