import { api } from '../api/client';
import type { Application, Configuration } from '../api/types';
import { setApplications, store, upsertApplication, upsertConfiguration } from './store';

export async function loadApplications() {
  store.set({ meta: { ...store.get().meta, loading: true, error: null } });
  try {
    const apps = await api.listApplications();
    // Sort by updatedAt desc (fallback id desc)
    apps.sort((a, b) => {
      const au = a.updatedAt ? Date.parse(a.updatedAt) : 0;
      const bu = b.updatedAt ? Date.parse(b.updatedAt) : 0;
      if (au !== bu) return bu - au;
      return b.id.localeCompare(a.id);
    });
    setApplications(apps);
  } catch (e: any) {
    store.set({ meta: { ...store.get().meta, loading: false, error: e?.message || 'Failed to load' } });
  }
}

export async function createApplicationOptimistic(input: Pick<Application, 'id' | 'name' | 'comments'>) {
  const token = `app-create-${input.id}-${Date.now()}`;
  store.snapshot(token);
  const optimistic: Application = { ...input, configuration_ids: [] };
  upsertApplication(optimistic);
  try {
    const created = await api.createApplication(input);
    upsertApplication(created);
    return { ok: true as const, token };
  } catch (e) {
    store.rollback(token);
    return { ok: false as const, token, error: e };
  }
}

export async function updateApplicationOptimistic(id: string, patch: Partial<Pick<Application, 'name' | 'comments'>>) {
  const token = `app-update-${id}-${Date.now()}`;
  store.snapshot(token);
  const current = store.get().applicationsById[id];
  if (current) upsertApplication({ ...current, ...patch });
  try {
    const updated = await api.updateApplication(id, patch);
    upsertApplication(updated);
    return { ok: true as const, token };
  } catch (e) {
    store.rollback(token);
    return { ok: false as const, token, error: e };
  }
}

export async function createConfigurationOptimistic(input: { id: string; application_id: string; name: string; comments?: unknown; config: Record<string, unknown> }) {
  const token = `cfg-create-${input.id}-${Date.now()}`;
  store.snapshot(token);
  const optimistic: Configuration = { ...input } as Configuration;
  upsertConfiguration(optimistic);
  try {
    const created = await api.createConfiguration(input);
    upsertConfiguration(created);
    return { ok: true as const, token };
  } catch (e) {
    store.rollback(token);
    return { ok: false as const, token, error: e };
  }
}

export async function updateConfigurationOptimistic(id: string, patch: Partial<Pick<Configuration, 'name' | 'comments' | 'config'>>) {
  const token = `cfg-update-${id}-${Date.now()}`;
  store.snapshot(token);
  const current = store.get().configurationsById[id];
  if (current) upsertConfiguration({ ...current, ...patch } as Configuration);
  try {
    const updated = await api.updateConfiguration(id, patch);
    upsertConfiguration(updated);
    return { ok: true as const, token };
  } catch (e) {
    store.rollback(token);
    return { ok: false as const, token, error: e };
  }
}
