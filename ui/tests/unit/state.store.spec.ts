import { describe, it, expect } from 'vitest';
import { store, upsertApplication } from '../../src/state/store';

describe('store', () => {
  it('upserts application and notifies subscribers', () => {
    let notified = false;
    const unsub = store.subscribe(() => { notified = true; });
    upsertApplication({ id: 'x', name: 'X' });
    expect(store.get().applicationsById['x'].name).toBe('X');
    expect(notified).toBe(true);
    unsub();
  });
});

