---
name: e2e-tests
description: Generate Playwright E2E tests for a page or feature based on the current project setup
argument-hint: [page-or-feature-name]
---

# Generate E2E Tests

Create Playwright E2E tests for `$ARGUMENTS` following the project's existing test patterns.

## Steps

1. **Read the existing test setup** — check `playwright.config.ts` and any existing tests in `tests/e2e/` to match the project's patterns
2. **Read the target page/component** — understand what needs to be tested
3. **Generate the test file** at `tests/e2e/$ARGUMENTS.spec.ts`

## Test Structure Template

```typescript
import { test, expect } from "@playwright/test";

test.describe("$ARGUMENTS", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/relevant-route");
  });

  // Navigation & Rendering
  test("should render the page correctly", async ({ page }) => {
    // Check key elements are visible
  });

  // User Interactions
  test("should handle [interaction]", async ({ page }) => {
    // Click, fill, submit etc.
  });

  // Form Validation (if applicable)
  test("should show validation errors for invalid input", async ({ page }) => {
    // Submit empty/invalid form, check error messages
  });

  test("should submit form successfully with valid data", async ({ page }) => {
    // Fill valid data, submit, check success state
  });

  // Responsive (if applicable)
  test("should work on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    // Check mobile-specific behavior
  });

  // Navigation
  test("should navigate correctly via CTA buttons", async ({ page }) => {
    // Click CTAs, verify navigation
  });
});
```

## Rules

- **Match existing patterns** — if there are already tests in the project, follow their style
- **Use data-testid** attributes when selecting elements — add them to components if missing
- **Test user flows**, not implementation details
- **Keep tests independent** — each test should work in isolation
- **No hardcoded waits** — use `waitForSelector`, `waitForResponse`, or Playwright auto-wait
- **Cover both happy path and error cases**
- **Mobile viewport tests** for responsive pages (375x812)
- **Check accessibility** — test keyboard navigation and aria attributes where relevant

## What to test per page type

### Landing Page
- All sections render (hero, features, CTA, footer)
- CTA buttons navigate correctly
- Newsletter/signup form validation + submission
- Mobile menu works
- Scroll behavior

### Survey / Multi-step Form
- Each screen renders correctly
- Forward/back navigation
- Input validation per screen
- Data persists between screens
- Final submission works
- Progress indicator updates

### Auth Pages
- Login/signup form validation
- Error messages for wrong credentials
- Redirect after successful auth
- Protected route redirect when not authenticated

## After generating

- Run `npm run test:e2e` to verify tests pass
- Add `data-testid` attributes to components if selectors are fragile
- Consider adding the tests to CI if not already configured
