// import { test, expect } from '@playwright/test';
// import { mockConfigurations, openApplications } from './_helpers';

// test.describe('Configurations CRUD', () => {
//   test('create configuration from app edit (with comments)', async ({ page }) => {
//     let created: any | null = null;
//     await mockConfigurations(page, { onCreate: p => (created = p) });
//     await openApplications(page);
//     await page.getByText('Alpha', { exact: true }).click();
//     await page.getByRole('link', { name: 'Add Configuration' }).click();
//     await expect(page).toHaveURL(/#\/applications\/alpha\/configs\/new$/);
//     const cfgForm = page.locator('config-form');
//     await cfgForm.locator('#id').fill('cfg2');
//     await cfgForm.locator('#application_id').fill('alpha');
//     await cfgForm.locator('#name').fill('Secondary');
//     await cfgForm.locator('#comments').fill('Secondary config comment');
//     await cfgForm.locator('button[type="submit"]').click();
//     await expect(page.getByText('Configuration created')).toBeVisible();
//     await expect(page).toHaveURL(/#\/applications\/alpha$/);
//     expect(created?.comments).toBe('Secondary config comment');
//   });

//   test('edit configuration via direct route (with comments)', async ({ page }) => {
//     let patch: any | null = null;
//     await mockConfigurations(page, { onUpdate: (_id, p) => (patch = p) });
//     await page.goto('/#/configurations/cfg1');
//     await expect(page.getByText('Save')).toBeVisible();
//     const cfgEditForm = page.locator('config-form');
//     await cfgEditForm.locator('#name').fill('Default Edited');
//     await cfgEditForm.locator('#comments').fill('Default edited comment');
//     await cfgEditForm.locator('button[type="submit"]').click();
//     await expect(page.getByText('Configuration saved')).toBeVisible();
//     expect(patch?.comments).toBe('Default edited comment');
//   });
// });
