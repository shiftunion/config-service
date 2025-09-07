- Prompt: Read @/prompts/1-web-api-specs.md and follow the instructions at the top of the file.
- Tool: ChatGPT
- Mode: Plan
- Context: Clean
- Model: Codex GPT-5
- Input: prompts/1-web-api-specs.md
- Output : prompts/2-web-api-prompt.md
- Cost: N/A
- Reflections:

### Create a plan based on the spec
- Prompt: Read @/prompts/2-web-api-prompt.md and follow the instructions at the top of the file.
- Mode: Plan
- Context: Clean
- Input: prompts/2-web-api-specs.md
- Output: prompts/3-web-api-plan.md

### App Generation: 1st pass with GPT5
- Prompt:  Please create a Config API Service in the `config-service` folder, according to the Implementation Plan defined in @/prompts/3-web-api-plan.md
- Tool: Codex
- Mode: Agent
- Context: N/A
- Model: GPT-5
- Input: prompts/3-web-api-plan.md && prompts/3a-out-gpt-5.md
- Output: config-service/

### App Generation - 2nd pass with Grok-fast-code
- Prompt:  Please create a Config API Service in the `config-service` folder, according to the Implementation Plan defined in @/prompts/3-web-api-plan.md
- Tool: Cline
- Mode: Agent
- Context: N/A
- Model: Grok Fast Code
- Input: prompts/3-web-api-plan.md
- Output: config-service/ & prompts/3b-out-grok-fast-code.md

### UI Generation - Plan creation with GPT-5
- Prompt:  Please create a Config API Service in the `config-service` folder, according to the Implementation Plan defined in @/prompts/4-admin-ui-prompt.md
- Tool: Codex
- Mode: Agent
- Output: @prompts/5-ui-plan.md
- **Reflections:**
  - generated a ENDPOINTS_SUMMARY summary file
  - uv run python scripts/generate_endpoint_summary.py > ENDPOINTS_SUMMARY.md
  - Considerations that couldbe added:
    - Deployment & CI/CD – define hosting approach, build/test gates, artifact publishing.
    - Developer Experience – onboarding docs, contribution guidelines, component demo route.
    - Configuration Management – environment variables, per-env config handling.
    - Error Handling & Logging – global error/telemetry strategy, not just UI states.
    - Accessibility Testing – automated a11y checks in CI (axe, Playwright a11y).
    - Security Hardening – CSP, inline script/style restrictions, sensitive config handling.
    - Performance Targets – load time, bundle size, lazy-loading.
    - Documentation – admin user guide, dev technical docs, known limitations.
    - Extensibility – pattern for adding new entity types, reusable components.

### Agentic Improvements iterations - Codex Agent, GPT-5, Cline+Grok-fast-code

    - Continually needed to be updating my ignore file
    - Did not have a configurable end point base. Added one
      - add a VITE_API_BASE env (e.g., https://api.example.com) and have the client prefix requests with it.
      - env.example
    - Playwright test did not build - missing dependencies
      - Playwrite tests did not run
    - Comments field was missing from UI listig - agent request via Codex fixed easily
    - Codex - seems to make up Playwright test cases for behaviour it thinks should be there
      - Playwrite generated test actually highlighted some functional gaps in my app that I wasn't aware of, where toast messages were not working
