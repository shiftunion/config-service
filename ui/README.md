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
- To point at a different host, set `VITE_API_BASE` at build/dev time.
- Example: copy `.env.example` to `.env` and edit:

  VITE_API_BASE=https://api.example.com

Notes:
- Ensure CORS is configured on the API if cross-origin.
- If the API requires cookies, add `credentials: 'include'` to `fetch` calls as needed.
