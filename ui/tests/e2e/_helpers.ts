import { Page, Route, Request, expect } from '@playwright/test';

export function json(data: any) {
  return { status: 200, contentType: 'application/json', body: JSON.stringify(data) } as const;
}

export async function mockApplications(
  page: Page,
  opts?: {
    onCreate?: (payload: any) => any;
    onUpdate?: (id: string, payload: any) => any;
    failNextCreate?: boolean;
    failNextUpdate?: boolean;
    seed?: Array<any>;
  }
) {
  let apps = opts?.seed ?? [
    { id: 'beta', name: 'Beta', comments: 'Beta comment', updatedAt: '2024-01-02T00:00:00Z' },
    { id: 'alpha', name: 'Alpha', comments: 'Alpha comment', updatedAt: '2024-01-01T00:00:00Z' }
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
      const found = apps.find(a => a.id === id) || { id, name: '', comments: '', updatedAt: '' };
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

  return { get apps() { return apps; } };
}

export async function mockConfigurations(
  page: Page,
  opts?: {
    onCreate?: (payload: any) => any;
    onUpdate?: (id: string, payload: any) => any;
    seedApps?: Array<any>;
    seedCfgs?: Array<any>;
  }
) {
  let apps = opts?.seedApps ?? [ { id: 'alpha', name: 'Alpha', comments: '', updatedAt: '2024-01-01T00:00:00Z' } ];
  let cfgs: any[] = opts?.seedCfgs ?? [ { id: 'cfg1', application_id: 'alpha', name: 'Default', comments: '', config: { a: 1 }, updatedAt: '2024-01-01T00:00:00Z' } ];

  await page.route('**/api/v1/applications', async (route: Route, req: Request) => {
    if (req.method() === 'GET') return route.fulfill(json(apps));
    if (req.method() === 'POST') { const payload = JSON.parse(req.postData() || '{}'); apps = [payload, ...apps]; return route.fulfill(json(payload)); }
    return route.fallback();
  });
  await page.route('**/api/v1/applications/*', async (route: Route, req: Request) => {
    const id = req.url().split('/').pop()!;
    if (req.method() === 'GET') return route.fulfill(json(apps.find(a => a.id === id) || { id, name: '', comments: '' }));
    if (req.method() === 'PUT') { const patch = JSON.parse(req.postData() || '{}'); const i = apps.findIndex(a => a.id === id); if (i>=0) apps[i] = { ...apps[i], ...patch }; return route.fulfill(json(apps[i])); }
    return route.fallback();
  });

  await page.route('**/api/v1/configurations', async (route: Route, req: Request) => {
    if (req.method() === 'POST') { const payload = JSON.parse(req.postData() || '{}'); const created = opts?.onCreate ? opts.onCreate(payload) : payload; cfgs = [created, ...cfgs]; return route.fulfill(json(created)); }
    return route.fallback();
  });
  await page.route('**/api/v1/configurations/*', async (route: Route, req: Request) => {
    const id = req.url().split('/').pop()!;
    if (req.method() === 'GET') return route.fulfill(json(cfgs.find(c => c.id === id) || { id, application_id: '', name: '', config: {} }));
    if (req.method() === 'PUT') { const patch = JSON.parse(req.postData() || '{}'); const i = cfgs.findIndex(c => c.id === id); if (i>=0) cfgs[i] = { ...cfgs[i], ...patch }; const updated = opts?.onUpdate ? opts.onUpdate(id, patch) : cfgs[i]; return route.fulfill(json(updated)); }
    return route.fallback();
  });

  return { get cfgs() { return cfgs; } };
}

export async function openApplications(page: Page) {
  await page.goto('/#/applications');
  // Assert on a unique element in the view to avoid strict-mode text collisions
  await expect(page.locator('app-table')).toBeVisible();
}
