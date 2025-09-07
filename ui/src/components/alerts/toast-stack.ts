type Toast = { id: string; kind: 'info'|'success'|'error'; text: string; timeout?: number };

export class ToastStack extends HTMLElement {
  #root: ShadowRoot;
  #toasts: Toast[] = [];
  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
    this.render();
  }
  push(t: Toast) {
    this.#toasts = [...this.#toasts, t];
    this.render();
    if (t.timeout) setTimeout(() => this.dismiss(t.id), t.timeout);
  }
  dismiss(id: string) {
    this.#toasts = this.#toasts.filter(x => x.id !== id);
    this.render();
  }
  render() {
    this.#root.innerHTML = `
      <style>
        :host { position: fixed; right: 16px; bottom: 16px; display: grid; gap: 8px; z-index: 1000; }
        .toast { background: var(--surface-1); border: 1px solid var(--border); color: var(--text); padding: 10px 12px; border-radius: 8px; box-shadow: var(--shadow-1); min-width: 240px; }
        .success { border-left: 4px solid var(--success); }
        .error { border-left: 4px solid var(--danger); }
        .info { border-left: 4px solid var(--primary); }
        button { background: transparent; border: none; color: var(--text-muted); float: right; cursor: pointer; }
      </style>
      ${this.#toasts.map(t => `
        <div class="toast ${t.kind}" role="status">
          <button aria-label="Dismiss" data-id="${t.id}">✕</button>
          <div>${t.text}</div>
        </div>
      `).join('')}
    `;
    this.#root.querySelectorAll('button[data-id]').forEach(btn => {
      btn.addEventListener('click', () => this.dismiss((btn as HTMLButtonElement).dataset.id!));
    });
  }
}

customElements.define('toast-stack', ToastStack);

