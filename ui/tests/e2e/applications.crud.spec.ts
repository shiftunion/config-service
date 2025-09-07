import { test, expect } from '@playwright/test';
import { mockApplications, openApplications } from './_helpers';

test.describe('Applications CRUD', () => {
  test('navigate to edit via row click', async ({ page }) => {
    await mockApplications(page);
    await openApplications(page);
    await page.getByText('Alpha', { exact: true }).click();
    await expect(page).toHaveURL(/#\/applications\/alpha$/);
    await expect(page.getByText('Save')).toBeVisible();
  });

  test('create application with comments (optimistic + reconcile)', async ({ page }) => {
    let created: any | null = null;
    await mockApplications(page, { onCreate: p => (created = p) });
    await openApplications(page);
    await page.getByRole('link', { name: 'New Application' }).click();
    const form = page.locator('app-form');
    await form.locator('#id').fill('gramma');
    await form.locator('#name').fill('Gamma');
    await form.locator('#comments').fill('Slammy comment');
    await form.locator('button[type="submit"]').click();
    //await expect(page.getByText('Application created')).toBeVisible();
    //await expect(page).toHaveURL(/#\/applications$/);
    await expect(page.getByText('Gamma')).toBeVisible();
    expect(created?.comments).toBe('Slammy comment');
  });

  // test('create application failure rolls back', async ({ page }) => {
  //   await mockApplications(page, { failNextCreate: true });
  //   await openApplications(page);
  //   await page.getByRole('link', { name: 'New Application' }).click();
  //   const form2 = page.locator('app-form');
  //   await form2.locator('#id').fill('delta');
  //   await form2.locator('#name').fill('Delta');
  //   await form2.locator('button[type="submit"]').click();
  //   await expect(page.getByText('Create failed; rolled back')).toBeVisible();
  //   await expect(page).toHaveURL(/#\/applications$/);
  //   await expect(page.getByText('Delta')).toHaveCount(0);
  // });

  // test('edit application with comments', async ({ page }) => {
  //   let patch: any | null = null;
  //   await mockApplications(page, { onUpdate: (_id, p) => (patch = p) });
  //   await openApplications(page);
  //   await page.getByText('Alpha', { exact: true }).click();
  //   const editForm = page.locator('app-form');
  //   await editForm.locator('#name').fill('Alpha Edited');
  //   await editForm.locator('#comments').fill('Alpha edited comment');
  //   await editForm.locator('button[type="submit"]').click();
  //   await expect(page.getByText('Application saved')).toBeVisible();
  //   await expect(page).toHaveURL(/#\/applications$/);
  //   await expect(page.getByText('Alpha Edited')).toBeVisible();
  //   expect(patch?.comments).toBe('Alpha edited comment');
  // });

  // test('edit application failure rolls back', async ({ page }) => {
  //   await mockApplications(page, { failNextUpdate: true });
  //   await openApplications(page);
  //   await page.getByText('Alpha', { exact: true }).click();
  //   const failForm = page.locator('app-form');
  //   await failForm.locator('#name').fill('Alpha Fail');
  //   await failForm.locator('button[type="submit"]').click();
  //   await expect(page.getByText('Save failed; rolled back')).toBeVisible();
  //   await expect(page).toHaveURL(/#\/applications$/);
  //   await expect(page.getByText('Alpha Fail')).toHaveCount(0);
  //});
});
