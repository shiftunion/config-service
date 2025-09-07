export class FormSkeleton extends HTMLElement {
  #root: ShadowRoot;
  constructor() { super(); this.#root = this.attachShadow({ mode: 'open' }); }
  connectedCallback() { this.render(); }
  render() {
    this.#root.innerHTML = `
      <style>
        .skel { height: 14px; background: linear-gradient(90deg, var(--surface-2) 25%, var(--surface-1) 37%, var(--surface-2) 63%); background-size: 400% 100%; animation: shimmer 1.4s ease infinite; border-radius: 4px; }
        @keyframes shimmer { 0% { background-position: 100% 0; } 100% { background-position: 0 0; } }
        .row { display: grid; gap: 8px; padding: 10px 0; }
      </style>
      <div class="card" style="padding: 12px;">
        ${Array.from({ length: 4 }).map(() => `<div class="row"><div class="skel"></div><div class="skel" style="height:32px"></div></div>`).join('')}
      </div>
    `;
  }
}

customElements.define('form-skeleton', FormSkeleton);

