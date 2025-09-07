import './components/app-shell/app-shell';
import './components/app-table/app-table';
import './components/app-form/app-form';
import './components/config-form/config-form';
import './components/skeletons/table-skeleton';
import './components/skeletons/form-skeleton';
import { Router } from './router';
import { loadApplications, createApplicationOptimistic, updateApplicationOptimistic, createConfigurationOptimistic, updateConfigurationOptimistic } from './state/queries';
import { store } from './state/store';
import { api } from './api/client';

function getShell(): any { return document.querySelector('app-shell') as any; }

function mountApplicationsList() {
  const shell = getShell();
  if (!shell?.outlet) return;
  shell.outlet.innerHTML = '';
  const card = document.createElement('div');
  card.className = 'card';
  card.style.padding = '12px';
  const toolbar = document.createElement('div');
  toolbar.className = 'toolbar';
  toolbar.innerHTML = `
    <div style="font-weight:600">Applications</div>
    <div>
      <a class="btn primary" href="#/applications/new">New Application</a>
    </div>
  `;
  card.appendChild(toolbar);
  const table = document.createElement('app-table') as any;
  (table as any).columns = [
    { key: 'id', header: 'ID' },
    { key: 'name', header: 'Name' },
    { key: 'updatedAt', header: 'Updated' }
  ];
  card.appendChild(table);
  shell.outlet.appendChild(card);

  const unsub = store.subscribe(s => {
    (table as any).items = s.applicationIds.map(id => s.applicationsById[id]);
  });
  table.addEventListener('row-activate', (e: any) => {
    const id = e.detail?.id;
    if (id) location.hash = `#/applications/${encodeURIComponent(id)}`;
  });
  loadApplications();
  const cleanup = () => unsub();
  window.addEventListener('hashchange', cleanup, { once: true });
}

function mountApplicationCreate() {
  const shell = getShell();
  if (!shell?.outlet) return;
  shell.outlet.innerHTML = '';
  const card = document.createElement('div'); card.className = 'card'; card.style.padding = '16px';
  const form = document.createElement('app-form') as any;
  form.data = { id: '', name: '', comments: '' };
  form.addEventListener('submit', async (e: any) => {
    const res = await createApplicationOptimistic({ id: e.detail.id, name: e.detail.name, comments: e.detail.comments });
    const toasts = document.querySelector('toast-stack') as any;
    if (res.ok) toasts?.push({ id: 'app-create', kind: 'success', text: 'Application created', timeout: 2500 });
    else toasts?.push({ id: 'app-create-err', kind: 'error', text: 'Create failed; rolled back', timeout: 4000 });
    location.hash = '#/applications';
  });
  form.addEventListener('cancel', () => history.back());
  card.appendChild(form); shell.outlet.appendChild(card);
}

function mountApplicationEdit(id: string) {
  const shell = getShell();
  if (!shell?.outlet) return;
  shell.outlet.innerHTML = '';
  const s = store.get();
  const app = s.applicationsById[id];
  const card = document.createElement('div'); card.className = 'card'; card.style.padding = '16px';
  const form = document.createElement('app-form') as any;
  form.data = { id, name: app?.name ?? '', comments: (app?.comments as any) ?? '' };
  form.addEventListener('submit', async (e: any) => {
    const res = await updateApplicationOptimistic(id, { name: e.detail.name, comments: e.detail.comments });
    const toasts = document.querySelector('toast-stack') as any;
    if (res.ok) toasts?.push({ id: 'app-update', kind: 'success', text: 'Application saved', timeout: 2000 });
    else toasts?.push({ id: 'app-update-err', kind: 'error', text: 'Save failed; rolled back', timeout: 4000 });
    location.hash = '#/applications';
  });
  form.addEventListener('cancel', () => history.back());
  const addCfg = document.createElement('a');
  addCfg.className = 'btn';
  addCfg.textContent = 'Add Configuration';
  addCfg.href = `#/applications/${encodeURIComponent(id)}/configs/new`;
  card.appendChild(form);
  card.appendChild(document.createElement('hr'));
  card.appendChild(addCfg);
  shell.outlet.appendChild(card);
}

const router = new Router();
router
  .add('/applications', () => mountApplicationsList())
  .add('/applications/new', () => mountApplicationCreate())
  .add('/applications/:id', ({ id }) => mountApplicationEdit(id))
  .add('/applications/:id/configs/new', ({ id }) => mountConfigCreate(id))
  .add('/configurations/:id', ({ id }) => mountConfigEdit(id))
  .notFound(() => { location.hash = '#/applications'; });

router.start();
(window as any).store = store;

function mountConfigCreate(appId: string) {
  const shell = getShell();
  if (!shell?.outlet) return;
  shell.outlet.innerHTML = '';
  const card = document.createElement('div'); card.className = 'card'; card.style.padding = '16px';
  const form = document.createElement('config-form') as any;
  form.data = { id: '', application_id: appId, name: '', comments: '', config: {} };
  form.addEventListener('submit', async (e: any) => {
    const { id, application_id, name, comments, config } = e.detail;
    const res = await createConfigurationOptimistic({ id, application_id, name, comments, config });
    const toasts = document.querySelector('toast-stack') as any;
    if (res.ok) toasts?.push({ id: 'cfg-create', kind: 'success', text: 'Configuration created', timeout: 2500 });
    else toasts?.push({ id: 'cfg-create-err', kind: 'error', text: 'Create failed; rolled back', timeout: 4000 });
    history.back();
  });
  form.addEventListener('cancel', () => history.back());
  card.appendChild(form); shell.outlet.appendChild(card);
}

function mountConfigEdit(cfgId: string) {
  const shell = getShell();
  if (!shell?.outlet) return;
  shell.outlet.innerHTML = '';
  const card = document.createElement('div'); card.className = 'card'; card.style.padding = '16px';
  const form = document.createElement('config-form') as any;
  const cfg = (window as any).store?.get?.().configurationsById?.[cfgId];
  form.data = cfg || { id: cfgId, application_id: '', name: '', comments: '', config: {} };
  if (!cfg) {
    api.getConfiguration(cfgId).then(c => { form.data = c as any; }).catch(() => {/* show error inline later */});
  }
  form.addEventListener('submit', async (e: any) => {
    const { name, comments, config } = e.detail;
    const res = await updateConfigurationOptimistic(cfgId, { name, comments, config });
    const toasts = document.querySelector('toast-stack') as any;
    if (res.ok) toasts?.push({ id: 'cfg-update', kind: 'success', text: 'Configuration saved', timeout: 2500 });
    else toasts?.push({ id: 'cfg-update-err', kind: 'error', text: 'Save failed; rolled back', timeout: 4000 });
    history.back();
  });
  form.addEventListener('cancel', () => history.back());
  card.appendChild(form); shell.outlet.appendChild(card);
}
