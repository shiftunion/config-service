import { test, expect } from '@playwright/test';

test.describe('Configurations CRUD (smoke)', () => {
  test('app boots', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('app-shell')).toBeVisible();
  });
});

