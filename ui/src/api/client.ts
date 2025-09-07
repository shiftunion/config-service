import type { Application, Configuration, ApiError } from './types';

const JSON_HEADERS = { 'Content-Type': 'application/json' } as const;
const API_BASE = (import.meta as any).env?.VITE_API_BASE ? String((import.meta as any).env.VITE_API_BASE).replace(/\/$/, '') : '';
const url = (path: string) => `${API_BASE}${path}`;

async function request<T>(input: RequestInfo, init?: RequestInit & { timeoutMs?: number }): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), init?.timeoutMs ?? 15000);
  try {
    const hasBody = !!(init && 'body' in init && (init as RequestInit).body != null);
    const headers = { ...(init?.headers || {}), ...(hasBody ? JSON_HEADERS : {}) } as Record<string, string>;
    const res = await fetch(input, { ...init, signal: controller.signal, headers });
    const text = await res.text();
    const data = text ? JSON.parse(text) : undefined;
    if (!res.ok) {
      const err = new Error(`HTTP ${res.status}`) as ApiError;
      err.status = res.status;
      err.details = data;
      throw err;
    }
    return data as T;
  } finally {
    clearTimeout(timeout);
  }
}

export const api = {
  async listApplications(): Promise<Application[]> {
    const data = await request<unknown>(url('/api/v1/applications'));
    if (Array.isArray(data)) return data as Application[];
    // Fallback if server wraps response
    if (data && typeof data === 'object' && 'items' in data && Array.isArray((data as any).items)) {
      return (data as any).items as Application[];
    }
    return [];
  },
  getApplication(id: string): Promise<Application> {
    return request<Application>(url(`/api/v1/applications/${encodeURIComponent(id)}`));
  },
  createApplication(input: Pick<Application, 'id' | 'name' | 'comments'>): Promise<Application> {
    return request<Application>(url('/api/v1/applications'), { method: 'POST', body: JSON.stringify(input) });
  },
  updateApplication(id: string, input: Partial<Pick<Application, 'name' | 'comments'>>): Promise<Application> {
    return request<Application>(url(`/api/v1/applications/${encodeURIComponent(id)}`), { method: 'PUT', body: JSON.stringify(input) });
  },
  getConfiguration(id: string): Promise<Configuration> {
    return request<Configuration>(url(`/api/v1/configurations/${encodeURIComponent(id)}`));
  },
  createConfiguration(input: { id: string; application_id: string; name: string; comments?: unknown; config: Record<string, unknown> }): Promise<Configuration> {
    return request<Configuration>(url('/api/v1/configurations'), { method: 'POST', body: JSON.stringify(input) });
  },
  updateConfiguration(id: string, input: Partial<Pick<Configuration, 'name' | 'comments' | 'config'>>): Promise<Configuration> {
    return request<Configuration>(url(`/api/v1/configurations/${encodeURIComponent(id)}`), { method: 'PUT', body: JSON.stringify(input) });
  }
};
