import { describe, it, expect, vi } from 'vitest';
import { api } from '../../src/api/client';

describe('api client', () => {
  it('parses array responses for listApplications', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => new Response(JSON.stringify([{ id: 'a', name: 'A' }]), { status: 200 })) as any);
    const apps = await api.listApplications();
    expect(apps[0].id).toBe('a');
  });
});

