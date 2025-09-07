import '../../styles/theme.css';
import '../alerts/toast-stack';

export class AppShell extends HTMLElement {
  #root: ShadowRoot;
  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  get outlet(): HTMLElement | null { return this.#root.querySelector('#outlet'); }
  render() {
    this.#root.innerHTML = `
      <style>
        header { position: sticky; top: 0; z-index: 10; background: var(--surface-1); border-bottom: 1px solid var(--border); }
        .nav { display: flex; align-items: center; gap: 12px; padding: 12px 16px; }
        .brand { font-weight: 600; color: var(--text); }
        main { display: block; padding: 16px; }
        .nav a { color: var(--text-muted); }
        .nav a.active { color: var(--text); }
      </style>
      <header class="card">
        <div class="nav container">
          <div class="brand">Config Admin</div>
          <nav style="margin-left:auto; display:flex; gap: 12px;">
            <a href="#/applications" data-link>Applications</a>
          </nav>
        </div>
      </header>
      <main>
        <div class="container">
          <div id="outlet"></div>
        </div>
      </main>
      <toast-stack></toast-stack>
    `;
  }
}

customElements.define('app-shell', AppShell);

