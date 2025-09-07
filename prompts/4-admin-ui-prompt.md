Create an implementation plan named `prompts/5-ui-plan.md` for an admin web interface that has features for adding and updating application entries as well as adding and updating the configuration name/value pairs.

- Use `prompts/ENDPOINTS_SUMMARY.md` to understand which endpoints and payloads are available.
- Use pnpm to manage dependencies and run scripts.
- All code should either be TypeScript, HTML, or CSS. Do not use JavaScript directly.
- Do not take any external dependencies, such as React and Vue, and use the Web Components functionality built into the browser. Also, only use the `fetch` feature of  modern browsers. The same principle applies to styling - only CSS and the Shadow DOM. 
- Automated testing is very important so ensure the plan includes unit testing with vitest and integration testing with Playwright.

**Tooling versions & test scaffolding**
- **Runtime/tooling**
  - Node 20.x, pnpm 9.x, TypeScript 5.x (strict mode), target `ES2022`, module `ESNext`
  - Browsers: latest 2 versions of Chrome/Edge/Firefox + Safari 16+

- **Visual Design**
  -  The site should take design cues from `https://www.devexpress.com/`, usign genral palet and fonts and design elements.
  -  Ensure a fully resposive design

- **UX behaviors**
  - Inline validation messages, optimistic UI for updates with rollback on failure
  - Table views with pagination (default pageSize=20), sort by `updatedAt desc` by default
  - Dedicated empty/loading/error states for lists and forms


