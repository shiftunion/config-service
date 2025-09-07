import { test, expect } from '@playwright/test';
import { mockApplications, openApplications } from './_helpers';

test('app boots and shows Applications', async ({ page }) => {
  await mockApplications(page);
  await openApplications(page);
  await expect(page.locator('app-shell')).toBeVisible();
});

