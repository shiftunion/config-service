# Config Admin UI

Dev server:
- pnpm install
- pnpm dev

Run unit tests:
- pnpm test:unit

Run e2e:
- pnpm build && pnpm preview
- pnpm test:e2e

Configuring API base URL:
- By default, the client uses same-origin paths like `/api/v1/...`.
- In dev, Vite proxies `/api` to `http://localhost:8000` (see `vite.config.ts`). Leave `VITE_API_BASE` unset to avoid CORS.
- To point at a different host (e.g., staging/production), set `VITE_API_BASE` at build/dev time.
- Example: copy `.env.example` to `.env` and edit:

  VITE_API_BASE=https://api.example.com

Notes:
- If you use `VITE_API_BASE` to point to another origin, ensure the API sends proper CORS headers (including handling `OPTIONS` preflight and allowing `Content-Type: application/json`).
- If the API requires cookies, add `credentials: 'include'` to `fetch` calls as needed.
