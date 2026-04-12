"""Form validation test templates."""

from __future__ import annotations

from sharingan.config import SharinganConfig
from sharingan.generate.test_planner import TestCase


def generate_form_tests(test_cases: list[TestCase], config: SharinganConfig) -> str:
    """Generate Playwright form test file.

    Args:
        test_cases: Form-related test cases.
        config: Sharingan configuration.

    Returns:
        Playwright test file content.
    """
    base_url = config.base_url
    lines = [
        'import { test, expect } from "@playwright/test";',
        "",
        f'const BASE_URL = "{base_url}";',
        "",
        'test.describe("Form Validation", () => {',
    ]

    for tc in test_cases:
        lines.append("")
        lines.append(f'  test("{_humanize(tc.name)}", async ({{ page }}) => {{')
        lines.append(f"    // {tc.description}")
        lines.append(f'    await page.goto(`${{BASE_URL}}{tc.route}`);')

        if "validation" in tc.name:
            lines.extend([
                "",
                "    // Submit form with empty fields to trigger validation",
                '    await page.getByRole("button", { name: /submit|save|send/i }).click();',
                "",
                "    // Expect validation error messages",
                '    await expect(page.getByText(/required|invalid|please/i)).toBeVisible();',
            ])
        elif "submission" in tc.name:
            lines.extend([
                "",
                "    // Fill in form fields with valid data",
                '    const inputs = page.locator("input:visible, textarea:visible, select:visible");',
                "    const count = await inputs.count();",
                "    for (let i = 0; i < count; i++) {",
                "      const input = inputs.nth(i);",
                '      const type = await input.getAttribute("type");',
                '      if (type === "email") {',
                '        await input.fill("test@example.com");',
                '      } else if (type === "password") {',
                '        await input.fill("SecurePass123!");',
                "      } else {",
                '        await input.fill("Test Value");',
                "      }",
                "    }",
                "",
                "    // Submit the form",
                '    await page.getByRole("button", { name: /submit|save|send/i }).click();',
                "",
                "    // Expect success indication",
                '    await expect(page.getByText(/success|saved|submitted|thank/i)).toBeVisible();',
            ])

        lines.append("  });")

    lines.append("});")
    lines.append("")
    return "\n".join(lines)


def _humanize(name: str) -> str:
    """Convert snake_case to human-readable test name."""
    return name.replace("_", " ").title()
