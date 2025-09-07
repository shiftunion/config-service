# Admin UI Implementation Plan (Web Components + TS)

## Goals
- Build an admin web interface to manage Applications and Configurations.
- Allow creating/updating Applications and their Configuration name/value pairs.
- Follow constraints: TypeScript/HTML/CSS only, Web Components + Shadow DOM, `fetch` only, no runtime UI libs.
- Provide robust UX: responsive layout, inline validation, optimistic updates with rollback, paginated/sortable tables, and clear empty/loading/error states.
- Ensure strong test coverage: unit tests with Vitest and integration/e2e with Playwright.

## API Surface (from `prompts/ENDPOINTS_SUMMARY.md`)
- Applications
  - `GET /api/v1/applications` – list applications
  - `POST /api/v1/applications` – create application
  - `GET /api/v1/applications/{id}` – get application
  - `PUT /api/v1/applications/{id}` – update application
- Configurations
  - `POST /api/v1/configurations` – create configuration
  - `GET /api/v1/configurations/{id}` – get configuration
  - `PUT /api/v1/configurations/{id}` – update configuration

Notes and assumptions:
- Responses show common fields `id`, `name`, `comments`, optional `configuration_ids` for applications, and `config` + `application_id` for configurations.
- Pagination/sorting support is not explicit in the summary. We will implement client‑side pagination/sorting first. If server adds `?page`/`?pageSize`/`?sort`, we’ll pass through and prefer server-side.
- Requirement asks for default sort by `updatedAt desc`. If `updatedAt` is not returned, we’ll surface a “backend field missing” banner and temporarily sort by `id desc` while logging a TODO to add `updatedAt` to responses.

## Tech & Tooling
- Runtime/targets: Node 20.x, TypeScript 5.x (strict), `ES2022`, module `ESNext`.
- Bundler/dev server: Vite (devDependency only) to compile TS and serve for Playwright. No runtime UI frameworks.
- Package manager: `pnpm`.
- Testing: Vitest (unit), Playwright (e2e/integration).
- Lint/format: ESLint (typescript-eslint) + Prettier (dev-only). Optional if already configured.

## Project Structure
```
ui/
  index.html
  src/
    main.ts
    router.ts               # minimal hash/history router (no deps)
    api/
      client.ts             # fetch wrapper + typed endpoints
      types.ts              # DTOs/interfaces mapped from summary
      schemas.ts            # runtime guards (narrowed types)
    state/
      store.ts              # simple reactive store (pub/sub)
      queries.ts            # loaders + cache + optimistic helpers
    components/
      app-shell/
        app-shell.ts        # layout, header, nav, theme
        app-shell.css
      app-table/
        app-table.ts        # generic table (pagination/sort/empty/error states)
        app-table.css
      app-form/
        app-form.ts         # application create/edit form
        app-form.css
      config-editor/
        config-editor.ts    # key/value editor for config object
        config-editor.css
      config-form/
        config-form.ts      # configuration create/edit form (wraps editor)
        config-form.css
      alerts/
        toast-stack.ts      # optimistic status + rollback messages
        inline-error.ts     # inline field error messages
      skeletons/
        table-skeleton.ts   # loading states
        form-skeleton.ts
    styles/
      tokens.css            # CSS variables (colors, spacing, typography)
      reset.css
      theme.css             # DevExpress-inspired palette
  tests/
    unit/
      api.client.spec.ts
      components.app-form.spec.ts
      components.config-editor.spec.ts
      state.store.spec.ts
    e2e/
      playwright.config.ts
      fixtures/
        mock-server.ts      # optional: route interception for Playwright
      app.crud.spec.ts
      config.crud.spec.ts
package.json
pnpm-lock.yaml
```

## Visual Design
- Take cues from devexpress.com: clean, high-contrast, generous spacing, subtle shadows.
- Implement CSS variables in `styles/tokens.css` (primary, accent, surface, text, success, warning, danger).
- Typography: system UI stack with weights/line heights echoing DevExpress density.
- Components use Shadow DOM to encapsulate styles, expose a small set of CSS parts for theming.
- Fully responsive: fluid grid, wrap tables on narrow screens with horizontal scroll + “sticky” header, stacked forms on mobile.

## UX Behaviors
- Inline validation: show beneath fields on blur and on submit; aria‑describedby for accessibility.
- Optimistic updates: immediately reflect local changes on create/update. On failure, rollback store and raise toast with retry.
- Tables: default pageSize=20, client-side pagination; default sort `updatedAt desc` (fallback as noted).
- States: explicit loading skeletons, empty messages, and inline error panels for lists/forms.

## Data Modeling (TypeScript)
- Application
  - `id: string`, `name: string`, `comments?: unknown`, `configuration_ids?: string[]`
  - Optional `updatedAt?: string` (planned; see assumptions)
- Configuration
  - `id: string`, `application_id: string`, `name: string`, `comments?: unknown`, `config: Record<string, unknown>`
- Narrowing/guards in `schemas.ts` to handle unknowns safely at runtime; surface decode errors.

## API Client (`api/client.ts`)
- Lightweight `request<T>(input, init)` wrapper: sets JSON headers, parses JSON, maps non‑2xx to typed errors, timeouts via `AbortController`.
- Methods:
  - `listApplications(): Promise<Application[]>`
  - `getApplication(id): Promise<Application>`
  - `createApplication(data: Pick<Application, 'id' | 'name' | 'comments'>): Promise<Application>`
  - `updateApplication(id, data: Partial<Pick<Application, 'name' | 'comments'>>): Promise<Application>`
  - `createConfiguration(data: { id: string; application_id: string; name: string; comments?: unknown; config: Record<string, unknown>; }): Promise<Configuration>`
  - `getConfiguration(id): Promise<Configuration>`
  - `updateConfiguration(id, data: Partial<Pick<Configuration, 'name' | 'comments' | 'config'>>): Promise<Configuration>`

## State & Data Fetching
- Small observable store with immutable updates and selectors (no external libs):
  - Caches: `applicationsById`, `configurationsById`.
  - Lists: `applicationIds`, `meta: { lastLoadedAt, loading, error }`.
  - Actions provide optimistic flow helpers: `applyOptimistic`, `rollback(token)`.
- `queries.ts` orchestrates list/detail loading, pagination, sorting, and optimistic mutations.

## Routing
- Minimal router using History API: routes
  - `/applications` – list
  - `/applications/new` – create
  - `/applications/:id` – edit
  - `/applications/:id/configs/new` – create configuration
  - `/configurations/:id` – edit configuration
- Router dispatches to view controllers that mount Web Components into the shell outlet.

## Components
- `app-shell`: header, nav, content outlet, toast stack, theme toggle.
- `app-table`: generic, supports columns, sorting, pagination, empty/loading/error slots.
- `app-form`: fields `name`, `comments`, submit/cancel, inline validation; emits `submit` with payload.
- `config-editor`: grid UI for key/value pairs; supports types string/number/boolean/json with validation; add/remove rows; import/export JSON.
- `config-form`: wraps `config-editor` plus `name`, `comments` and links to related application.
- `skeletons`: shimmer skeletons for table/form while loading.

## Validation
- Client-side rules:
  - Required: `name`, IDs on create; `application_id` for configurations.
  - Names: trim, length 1–120, no leading/trailing whitespace.
  - Config keys: non-empty, unique per configuration; values must be valid JSON primitives or objects.
- Server errors: map 422 to field messages when possible, else show top-level error.

## Optimistic UI & Rollback
- On create/update:
  - Snapshot previous state with a rollback token.
  - Apply optimistic change to store; update table/form immediately.
  - If request fails, rollback via token and show toast with error + “Retry”.
  - If success returns canonical server object, reconcile store (handles server-side defaults).

## Empty/Loading/Error States
- Lists: skeleton while loading; empty view with CTA to create; inline retry on error.
- Forms: skeleton for edit fetch; descriptive empty/error boundaries.

## Accessibility
- Keyboard focus order, roving focus for tables.
- `aria-live` region for toasts and validation feedback.
- Color contrast meets WCAG AA using tokenized palette.

## Security
- `fetch` with `same-origin` credentials when needed; CSRF header if backend uses it.
- Sanitize rendered strings; never dangerously set HTML; treat `comments` as plain text.

## Performance
- Lazy render of large tables via pagination; avoid heavy DOM in Shadow roots.
- Cache GET responses; revalidate on focus/interval for staleness as needed.

## Scripts (pnpm)
- `dev`: Vite dev server
- `build`: Vite build (ES modules)
- `preview`: Vite preview (for Playwright)
- `test`: `vitest run`
- `test:unit`: `vitest --run`
- `test:e2e`: `playwright test`
- `lint`/`format`: optional

## Testing Strategy
- Unit (Vitest):
  - `api/client.spec.ts`: happy path/error mapping, timeouts, guards.
  - Components: form validation, events emitted, optimistic flow behavior with mocked store.
  - Store: reducers, optimistic apply/rollback determinism.
- Integration/E2E (Playwright):
  - Launch built app with `pnpm preview`.
  - Stub network via route interception: successful create/update and failure cases.
  - Scenarios:
    - List applications: pagination/sort behavior, empty/loading/error.
    - Create application: inline validation, optimistic add, rollback on 422/500.
    - Edit application: change name/comments with optimistic update + reconcile.
    - Create configuration: add multiple key/values, type validation, optimistic creation.
    - Edit configuration: change keys/values, rollback on failure.

## Delivery Milestones
1) Scaffolding: Vite + TS + pnpm scripts, base styles, tokens, shell.
2) API client, types, guards; store with optimistic utilities.
3) Applications list: table with pagination/sort + states.
4) Application form: create/edit with inline validation + optimistic flow.
5) Configuration editor + form: create/edit + validation + optimistic flow.
6) Routing integration and navigation, cross-linking between app/config.
7) Unit tests for client/store/components; Playwright E2E for key flows.
8) Polish: responsive refinements, a11y audit, error messages, docs.

## Risks & Mitigations
- Missing `updatedAt`: add fallback sort and surface a banner; coordinate backend change.
- No server pagination: start client-side; transparently adopt server params if added.
- `comments`/`config` types are `unknown`/`object`: validate and guard at boundaries; keep UI resilient to shape.

## Acceptance Criteria
- Can list, create, and update Applications.
- Can create and update Configurations (name/value pairs) attached to Applications.
- Default table view shows sorted and paginated results with proper states.
- Optimistic UI with working rollback on simulated failures.
- Unit and E2E tests cover critical paths and pass in CI locally.
