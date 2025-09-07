export class InlineError extends HTMLElement {
  static get observedAttributes() { return ['message']; }
  #root: ShadowRoot;
  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
  }
  connectedCallback() { this.render(); }
  attributeChangedCallback() { this.render(); }
  set message(v: string | null) { if (v == null) this.removeAttribute('message'); else this.setAttribute('message', v); }
  get message() { return this.getAttribute('message'); }
  render() {
    const msg = this.message;
    this.#root.innerHTML = `
      <style>
        :host { display: ${msg ? 'block' : 'none'}; color: var(--danger); font-size: 12px; }
      </style>
      <span role="alert">${msg ?? ''}</span>
    `;
  }
}

customElements.define('inline-error', InlineError);

