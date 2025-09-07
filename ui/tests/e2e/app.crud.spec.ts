import { test, expect } from '@playwright/test';

test.describe('Applications CRUD (smoke)', () => {
  test('navigates to applications list', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('text=Applications')).toBeVisible();
  });
});

