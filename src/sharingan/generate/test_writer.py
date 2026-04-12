"""Generate Playwright test code from test plans."""

from __future__ import annotations

from sharingan.config import SharinganConfig
from sharingan.generate.templates import api, auth, crud, forms, navigation, accessibility
from sharingan.generate.test_planner import TestCase


def generate_test_file(test_cases: list[TestCase], category: str, config: SharinganConfig) -> str:
    """Generate a Playwright test file for a category of tests.

    Args:
        test_cases: List of test cases to include.
        category: Test category (auth, navigation, form, api, permission, accessibility).
        config: Sharingan configuration.

    Returns:
        Generated Playwright test file content as a string.
    """
    generators = {
        "auth": auth.generate_auth_tests,
        "navigation": navigation.generate_navigation_tests,
        "form": forms.generate_form_tests,
        "api": api.generate_api_tests,
        "permission": navigation.generate_permission_tests,
        "accessibility": accessibility.generate_accessibility_tests,
    }

    generator = generators.get(category, navigation.generate_navigation_tests)
    return generator(test_cases, config)
