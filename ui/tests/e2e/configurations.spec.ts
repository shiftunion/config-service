import { test, expect, Page, Route, Request } from '@playwright/test';

function json(data: any) {
  return { status: 200, contentType: 'application/json', body: JSON.stringify(data) } as const;
}

async function mockAll(page: Page) {
  let apps = [ { id: 'alpha', name: 'Alpha', updatedAt: '2024-01-01T00:00:00Z' } ];
  let cfgs: any[] = [ { id: 'cfg1', application_id: 'alpha', name: 'Default', comments: '', config: { a: 1 }, updatedAt: '2024-01-01T00:00:00Z' } ];

  await page.route('**/api/v1/applications', async (route: Route, req: Request) => {
    if (req.method() === 'GET') return route.fulfill(json(apps));
    if (req.method() === 'POST') { const payload = JSON.parse(req.postData() || '{}'); apps = [payload, ...apps]; return route.fulfill(json(payload)); }
    return route.fallback();
  });
  await page.route('**/api/v1/applications/*', async (route: Route, req: Request) => {
    const id = req.url().split('/').pop()!;
    if (req.method() === 'GET') return route.fulfill(json(apps.find(a => a.id === id) || { id, name: '' }));
    if (req.method() === 'PUT') { const patch = JSON.parse(req.postData() || '{}'); const i = apps.findIndex(a => a.id === id); if (i>=0) apps[i] = { ...apps[i], ...patch }; return route.fulfill(json(apps[i])); }
    return route.fallback();
  });

  await page.route('**/api/v1/configurations', async (route: Route, req: Request) => {
    if (req.method() === 'POST') { const payload = JSON.parse(req.postData() || '{}'); cfgs = [payload, ...cfgs]; return route.fulfill(json(payload)); }
    return route.fallback();
  });
  await page.route('**/api/v1/configurations/*', async (route: Route, req: Request) => {
    const id = req.url().split('/').pop()!;
    if (req.method() === 'GET') return route.fulfill(json(cfgs.find(c => c.id === id) || { id, application_id: '', name: '', config: {} }));
    if (req.method() === 'PUT') { const patch = JSON.parse(req.postData() || '{}'); const i = cfgs.findIndex(c => c.id === id); if (i>=0) cfgs[i] = { ...cfgs[i], ...patch }; return route.fulfill(json(cfgs[i])); }
    return route.fallback();
  });
}

test.describe('Configurations flows', () => {
  test.beforeEach(async ({ page }) => { await mockAll(page); });

  test('create configuration from application edit view', async ({ page }) => {
    await page.goto('/#/applications');
    await page.getByText('Alpha').click();
    await page.getByRole('link', { name: 'Add Configuration' }).click();
    await expect(page).toHaveURL(/#\/applications\/alpha\/configs\/new$/);
    await page.fill('config-form >> shadow=#id', 'cfg2');
    await page.fill('config-form >> shadow=#application_id', 'alpha');
    await page.fill('config-form >> shadow=#name', 'Secondary');
    // edit config editor rows: just add a row via internal button then set fields
    await page.click('config-form >> shadow=config-editor >> shadow=button[data-act="add"]');
    await page.fill('config-form >> shadow=config-editor >> shadow=tbody tr:nth-child(1) input[data-f="key"]', 'x');
    await page.fill('config-form >> shadow=config-editor >> shadow=tbody tr:nth-child(1) input[data-f="value"]', '1');
    await page.click('config-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Configuration created')).toBeVisible();
    await expect(page).toHaveURL(/#\/applications\/alpha$/);
  });

  test('edit configuration via direct route', async ({ page }) => {
    await page.goto('/#/configurations/cfg1');
    await expect(page.getByText('Save')).toBeVisible();
    await page.fill('config-form >> shadow=#name', 'Default Edited');
    await page.click('config-form >> shadow=button[type="submit"]');
    await expect(page.getByText('Configuration saved')).toBeVisible();
  });
});

