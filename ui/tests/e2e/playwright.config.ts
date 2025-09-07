import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'pnpm build && pnpm preview',
    port: 5173,
    reuseExistingServer: true,
    timeout: 120000
  },
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry'
  }
});
