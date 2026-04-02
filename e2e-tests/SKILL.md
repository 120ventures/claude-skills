---
name: e2e-tests
description: Generate Playwright E2E tests for a page or feature based on the current project setup
argument-hint: [page-or-feature-name]
---

# Generate E2E Tests

Create Playwright E2E tests for `$ARGUMENTS` following the Herbalance reference architecture.

## Step 1: Infrastructure Check

Before generating any tests, check if the test infrastructure exists:

```
playwright.config.ts
tests/e2e/setup/global-setup.ts
tests/e2e/fixtures/test-base.ts
tests/e2e/helpers/viewport.helper.ts
tests/e2e/helpers/navigation.helper.ts
```

- If ALL files exist: skip to Step 3
- If ANY file is missing: ask the user "Test-Infrastruktur fehlt oder ist unvollstaendig. Soll ich sie aufsetzen?" - only proceed to Step 2 after confirmation

## Step 2: Generate Infrastructure

Only run this step if the user confirmed in Step 1.

### 2a. Install dependencies

```bash
npm install -D @playwright/test dotenv @supabase/supabase-js
npx playwright install
```

### 2b. Add npm scripts to package.json

Add these scripts (don't overwrite existing ones):

```json
{
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:headed": "playwright test --headed",
  "test:e2e:debug": "playwright test --debug",
  "test:e2e:report": "playwright show-report"
}
```

### 2c. playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';
import dotenv from 'dotenv';

dotenv.config({ path: '.env.test', quiet: true });

export default defineConfig({
  testDir: './tests/e2e',
  globalSetup: './tests/e2e/setup/global-setup.ts',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [['html'], ['list']],
  timeout: 60000,
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 30000,
  },
  projects: process.env.CI
    ? [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
        { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
        { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
      ]
    : [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
      ],
  webServer: {
    command: 'npm run dev -- --mode test --port 5173',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

### 2d. tests/e2e/setup/global-setup.ts

```typescript
import { FullConfig } from '@playwright/test';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs/promises';

const execAsync = promisify(exec);

async function globalSetup(config: FullConfig) {
  console.log('Starting test setup...');

  // Check if Supabase is running, start if not
  let supabaseRunning = false;
  try {
    await execAsync('supabase status');
    supabaseRunning = true;
    console.log('Supabase is already running');
  } catch {
    console.log('Supabase is not running, starting it...');
  }

  if (!supabaseRunning) {
    try {
      await execAsync('supabase start');
      console.log('Supabase started successfully');
    } catch (error) {
      console.error('Failed to start Supabase:', error);
      throw error;
    }
  }

  // Check if .env.test file exists
  try {
    await fs.access('.env.test');
  } catch {
    throw new Error('.env.test file is required but not found.');
  }
}

export default globalSetup;
```

### 2e. tests/e2e/fixtures/test-base.ts

Adapt the session key name to the current project (use `<project-slug>_session_id`).

```typescript
import { test as base } from '@playwright/test';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

type TestFixtures = {
  supabase: SupabaseClient;
  sessionId: string;
};

export const test = base.extend<TestFixtures>({
  supabase: async ({}, use) => {
    const supabaseUrl = process.env.VITE_SUPABASE_URL!;
    const supabaseKey = process.env.VITE_SUPABASE_PUBLISHABLE_KEY!;
    if (!supabaseUrl || !supabaseKey) {
      throw new Error('Supabase environment variables not set.');
    }
    const supabase = createClient(supabaseUrl, supabaseKey);
    await use(supabase);
  },

  sessionId: async ({ page }, use) => {
    const sessionId = `test-session-${Date.now()}-${Math.random().toString(36).substring(7)}`;
    await page.addInitScript((id) => {
      localStorage.setItem('<project-slug>_session_id', id);
    }, sessionId);
    await use(sessionId);
  },
});

export { expect } from '@playwright/test';
```

### 2f. tests/e2e/helpers/viewport.helper.ts

```typescript
import { Page } from '@playwright/test';

export class ViewportHelper {
  constructor(private page: Page) {}

  async getVisibleHeader() {
    return this.page.locator('header').filter({ visible: true }).first();
  }
}
```

### 2g. tests/e2e/helpers/navigation.helper.ts

Adapt button texts and routes to the current project.

```typescript
import { Page } from '@playwright/test';
import { ViewportHelper } from './viewport.helper';

export class NavigationHelper {
  private viewportHelper: ViewportHelper;

  constructor(private page: Page) {
    this.viewportHelper = new ViewportHelper(page);
  }

  async navigateToPage(isMobile: boolean, buttonText: string) {
    const header = await this.viewportHelper.getVisibleHeader();
    if (isMobile) {
      await header.locator('button[aria-label="Menu"]').click();
    }
    await header.locator(`button:has-text("${buttonText}")`).click();
  }
}
```

## Step 3: Generate Tests for Feature

1. **Read existing tests** in `tests/e2e/` to match the project's established patterns
2. **Read the target page/component** to understand what needs testing
3. **Generate Helper class** at `tests/e2e/helpers/[feature].helper.ts` using Page Object Model
4. **Generate Spec file** at `tests/e2e/[feature].spec.ts`
5. **Run tests** with `npm run test:e2e`
6. **Add `data-testid` attributes** to components where selectors are fragile

### Helper Class Pattern

Helpers encapsulate page interactions. They receive `page` and optionally `supabase` in the constructor.

```typescript
import { Page } from '@playwright/test';
import { SupabaseClient } from '@supabase/supabase-js';
import { ViewportHelper } from './viewport.helper';

export class FeatureHelper {
  private viewportHelper: ViewportHelper;

  constructor(
    private page: Page,
    private supabase?: SupabaseClient
  ) {
    this.viewportHelper = new ViewportHelper(page);
  }

  // Encapsulate multi-step user flows
  async completeFlow() { /* ... */ }

  // Provide verification methods
  async verifyState() { /* ... */ }

  // Use edge functions for backend state when needed
  async getStateFromDB(sessionId: string) {
    const { data } = await this.supabase!.functions.invoke('get-state', {
      headers: { 'x-session-id': sessionId }
    });
    return data;
  }
}
```

### Spec File Pattern

```typescript
import { test, expect } from './fixtures/test-base';
import { FeatureHelper } from './helpers/feature.helper';
import { ViewportHelper } from './helpers/viewport.helper';

test.describe('Feature Name', () => {
  let featureHelper: FeatureHelper;
  let viewportHelper: ViewportHelper;

  test.beforeEach(async ({ page, supabase }) => {
    featureHelper = new FeatureHelper(page, supabase);
    viewportHelper = new ViewportHelper(page);
  });

  // Rendering
  test('should render correctly', async ({ page }) => {
    await page.goto('/route');
    // Check key elements
  });

  // User interactions
  test('should handle [interaction]', async ({ page }) => {
    // Use helper for multi-step flows
  });

  // Form validation (if applicable)
  test('should show validation errors', async ({ page }) => { /* ... */ });
  test('should submit successfully', async ({ page }) => { /* ... */ });

  // Mobile
  test('should work on mobile', async ({ page, isMobile }) => {
    if (!isMobile) test.skip();
    // Mobile-specific behavior
  });

  // Backend verification (if applicable)
  test('should persist data', async ({ page, supabase, sessionId }) => {
    // Use helper to verify DB state via edge functions
  });
});
```

## What to Test per Page Type

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

### E-Commerce / Cart
- Add/remove products
- Quantity updates (increment/decrement)
- Cart state persists (verify via edge function)
- Bundle/pricing selection
- Checkout flow

## Rules

- **Always import from `./fixtures/test-base`**, never directly from `@playwright/test`
- **Page Object Model** - all page interactions go through Helper classes
- **Use `data-testid`** for element selection - add them to components if missing
- **Test user flows**, not implementation details
- **Keep tests independent** - each test works in isolation
- **No `waitForTimeout`** - use `waitForSelector`, `waitForURL`, `waitForLoadState`, or Playwright auto-wait
- **Cover happy path and error cases**
- **Mobile viewport tests** for responsive pages
- **Accessibility** - test keyboard navigation and ARIA attributes where relevant
- **Backend verification** via Supabase edge functions, not direct DB queries
