import { test, expect, Page, Route, Request } from '@playwright/test';

function json(data: any) {
  return { status: 200, contentType: 'application/json', body: JSON.stringify(data) } as const;
}

async function mockApplications(page: Page, opts?: { onCreate?: (payload: any) => any; onUpdate?: (id: string, payload: any) => any; failNextCreate?: boolean; failNextUpdate?: boolean; }) {
  let apps = [
    { id: 'beta', name: 'Beta', updatedAt: '2024-01-02T00:00:00Z' },
    { id: 'alpha', name: 'Alpha', updatedAt: '2024-01-01T00:00:00Z' }
  ];

  await page.route('**/api/v1/applications', async (route: Route, req: Request) => {
    if (req.method() === 'GET') return route.fulfill(json(apps));
    if (req.method() === 'POST') {
      if (opts?.failNextCreate) { opts.failNextCreate = false; return route.fulfill({ status: 500, body: 'boom' }); }
      const payload = JSON.parse(req.postData() || '{}');
      const created = opts?.onCreate ? opts.onCreate(payload) : payload;
      apps = [created, ...apps];
      return route.fulfill(json(created));
    }
    return route.fallback();
  });

  await page.route('**/api/v1/applications/*', async (route: Route, req: Request) => {
    const id = req.url().split('/').pop()!;
    if (req.method() === 'GET') {
      const found = apps.find(a => a.id === id) || { id, name: '', updatedAt: '' };
      return route.fulfill(json(found));
    }
    if (req.method() === 'PUT') {
      if (opts?.failNextUpdate) { opts.failNextUpdate = false; return route.fulfill({ status: 500, body: 'boom' }); }
      const patch = JSON.parse(req.postData() || '{}');
      const idx = apps.findIndex(a => a.id === id);
      if (idx >= 0) apps[idx] = { ...apps[idx], ...patch };
      const updated = opts?.onUpdate ? opts.onUpdate(id, patch) : apps[idx];
      return route.fulfill(json(updated));
    }
    return route.fallback();
  });
}

test.describe('Applications flows', () => {
  test.beforeEach(async ({ page }) => {
    await mockApplications(page);
  });

  test('list and navigate to edit by row click', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByText('Applications')).toBeVisible();
    await page.getByText('Alpha').click();
    await expect(page).toHaveURL(/#\/applications\/alpha$/);
    await expect(page.getByText('Save')).toBeVisible();
  });

  test('create application success (optimistic + reconcile)', async ({ page }) => {
    await page.goto('/#/applications');
    await page.getByRole('link', { name: 'New Application' }).click();
    await expect(page).toHaveURL(/#\/applications\/new$/);
    await page.fill('app-form >> shadow=#id', 'gamma');
    await page.fill('app-form >> shadow=#name', 'Gamma');
    await page.click('app-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Application created')).toBeVisible();
    await expect(page).toHaveURL(/#\/applications$/);
    await expect(page.getByText('Gamma')).toBeVisible();
  });

  test('create application failure rolls back and shows error toast', async ({ page }) => {
    await mockApplications(page, { failNextCreate: true });
    await page.goto('/#/applications');
    await page.getByRole('link', { name: 'New Application' }).click();
    await page.fill('app-form >> shadow=#id', 'delta');
    await page.fill('app-form >> shadow=#name', 'Delta');
    await page.click('app-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Create failed; rolled back')).toBeVisible();
    await expect(page).toHaveURL(/#\/applications$/);
    await expect(page.getByText('Delta')).toHaveCount(0);
  });

  test('edit application success', async ({ page }) => {
    await page.goto('/#/applications');
    await page.getByText('Alpha').click();
    await page.fill('app-form >> shadow=#name', 'Alpha Edited');
    await page.click('app-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Application saved')).toBeVisible();
    await expect(page).toHaveURL(/#\/applications$/);
    await expect(page.getByText('Alpha Edited')).toBeVisible();
  });

  test('edit application failure rolls back', async ({ page }) => {
    await mockApplications(page, { failNextUpdate: true });
    await page.goto('/#/applications');
    await page.getByText('Alpha').click();
    await page.fill('app-form >> shadow=#name', 'Alpha Fail');
    await page.click('app-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Save failed; rolled back')).toBeVisible();
    await expect(page).toHaveURL(/#\/applications$/);
    await expect(page.getByText('Alpha Fail')).toHaveCount(0);
  });
});

