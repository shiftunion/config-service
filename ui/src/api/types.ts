export interface Application {
  id: string;
  name: string;
  comments?: unknown;
  configuration_ids?: string[];
  updatedAt?: string; // optional; backend may add later
}

export interface Configuration {
  id: string;
  application_id: string;
  name: string;
  comments?: unknown;
  config: Record<string, unknown>;
  updatedAt?: string;
}

export interface ApiError extends Error {
  status: number;
  details?: unknown;
}

