import type { Application, Configuration } from '../api/types';

type State = {
  applicationsById: Record<string, Application>;
  applicationIds: string[];
  configurationsById: Record<string, Configuration>;
  meta: { loading: boolean; error: string | null; lastLoadedAt?: number };
};

type Listener = (state: Readonly<State>) => void;

const initial: State = {
  applicationsById: {},
  applicationIds: [],
  configurationsById: {},
  meta: { loading: false, error: null }
};

let state: State = structuredClone(initial);
const listeners = new Set<Listener>();

type Snapshot = State;
const history = new Map<string, Snapshot>();

export const store = {
  get(): Readonly<State> { return state; },
  subscribe(fn: Listener) { listeners.add(fn); return () => listeners.delete(fn); },
  set(partial: Partial<State>) {
    state = { ...state, ...partial, meta: { ...state.meta, ...(partial as any).meta } };
    listeners.forEach(l => l(Object.freeze(structuredClone(state))));
  },
  reset() { state = structuredClone(initial); listeners.forEach(l => l(Object.freeze(structuredClone(state)))); },
  // optimistic
  snapshot(token: string) { history.set(token, structuredClone(state)); },
  rollback(token: string) { const snap = history.get(token); if (snap) { state = snap; history.delete(token); listeners.forEach(l => l(Object.freeze(structuredClone(state)))); } }
};

// Helpers
export function upsertApplication(app: Application) {
  const byId = { ...store.get().applicationsById, [app.id]: app };
  const ids = Array.from(new Set([...store.get().applicationIds, app.id]));
  store.set({ applicationsById: byId, applicationIds: ids });
}

export function setApplications(apps: Application[]) {
  const byId: Record<string, Application> = {};
  const ids: string[] = [];
  for (const a of apps) { byId[a.id] = a; ids.push(a.id); }
  store.set({ applicationsById: byId, applicationIds: ids, meta: { ...store.get().meta, lastLoadedAt: Date.now(), loading: false, error: null } });
}

export function upsertConfiguration(cfg: Configuration) {
  const byId = { ...store.get().configurationsById, [cfg.id]: cfg };
  store.set({ configurationsById: byId });
}
