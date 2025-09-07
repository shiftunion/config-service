import '../alerts/inline-error';
import '../config-editor/config-editor';

type FormData = { id?: string; application_id: string; name: string; comments?: string; config: Record<string, unknown> };

export class ConfigForm extends HTMLElement {
  #root: ShadowRoot;
  #data: FormData = { application_id: '', name: '', config: {} };
  #mode: 'create' | 'edit' = 'create';
  #errors: Partial<Record<keyof FormData, string>> = {};
  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
  }
  set data(d: FormData) { this.#data = { ...d }; this.#mode = d.id ? 'edit' : 'create'; this.render(); }
  get data() { return this.#data; }
  connectedCallback() { this.render(); }

  validate(): boolean {
    const e: typeof this.#errors = {};
    const name = (this.#root.querySelector('#name') as HTMLInputElement)?.value?.trim() ?? '';
    const appId = (this.#root.querySelector('#application_id') as HTMLInputElement)?.value?.trim() ?? '';
    if (!name) e.name = 'Name is required';
    if (!appId) e.application_id = 'Application ID is required';
    this.#errors = e; this.renderErrors();
    return Object.keys(e).length === 0;
  }
  private renderErrors() {
    (this.#root.querySelector('#nameErr') as any).message = this.#errors.name ?? '';
    (this.#root.querySelector('#appErr') as any).message = this.#errors.application_id ?? '';
  }
  render() {
    this.#root.innerHTML = `
      <style> form { display: grid; gap: 12px; } </style>
      <form novalidate>
        ${this.#mode === 'create' ? `
        <div class="field">
          <label for="id">ID</label>
          <input id="id" name="id" value="${this.#data.id ?? ''}" />
        </div>` : ''}
        <div class="field">
          <label for="application_id">Application ID</label>
          <input id="application_id" name="application_id" value="${this.#data.application_id ?? ''}" />
          <inline-error id="appErr"></inline-error>
        </div>
        <div class="field">
          <label for="name">Name</label>
          <input id="name" name="name" value="${this.#data.name ?? ''}" />
          <inline-error id="nameErr"></inline-error>
        </div>
        <div class="field">
          <label for="comments">Comments</label>
          <textarea id="comments" name="comments">${(this.#data.comments ?? '') as string}</textarea>
        </div>
        <div class="field">
          <label>Configuration</label>
          <config-editor id="editor"></config-editor>
        </div>
        <div style="display:flex; gap: 8px;">
          <button type="submit" class="btn primary">${this.#mode === 'create' ? 'Create' : 'Save'}</button>
          <button type="button" class="btn ghost" id="cancel">Cancel</button>
        </div>
      </form>
    `;
    (this.#root.querySelector('#editor') as any).value = this.#data.config || {};
    const form = this.#root.querySelector('form')!;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!this.validate()) return;
      const id = (this.#root.querySelector('#id') as HTMLInputElement)?.value?.trim();
      const application_id = (this.#root.querySelector('#application_id') as HTMLInputElement).value.trim();
      const name = (this.#root.querySelector('#name') as HTMLInputElement).value.trim();
      const comments = (this.#root.querySelector('#comments') as HTMLTextAreaElement).value || undefined;
      const config = (this.#root.querySelector('#editor') as any).value as Record<string, unknown>;
      const payload: FormData = { id: id || this.#data.id, application_id, name, comments, config };
      this.dispatchEvent(new CustomEvent('submit', { detail: payload }));
    });
    this.#root.querySelector('#cancel')?.addEventListener('click', () => this.dispatchEvent(new Event('cancel')));
  }
}

customElements.define('config-form', ConfigForm);

