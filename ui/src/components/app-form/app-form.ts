import '../alerts/inline-error';

type FormData = { id?: string; name: string; comments?: string };

export class AppForm extends HTMLElement {
  #root: ShadowRoot;
  #data: FormData = { name: '' };
  #errors: Partial<Record<keyof FormData, string>> = {};
  #mode: 'create' | 'edit' = 'create';

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
    if (!name) e.name = 'Name is required';
    if (name.length > 120) e.name = 'Name must be <= 120 chars';
    const id = (this.#root.querySelector('#id') as HTMLInputElement)?.value?.trim();
    if (this.#mode === 'create' && !id) e.id = 'ID is required';
    this.#errors = e;
    this.renderErrors();
    return Object.keys(e).length === 0;
  }

  private renderErrors() {
    const idErr = this.#root.querySelector('inline-error#idErr') as any;
    const nameErr = this.#root.querySelector('inline-error#nameErr') as any;
    idErr && (idErr.message = this.#errors.id ?? '');
    nameErr && (nameErr.message = this.#errors.name ?? '');
  }

  render() {
    this.#root.innerHTML = `
      <style>
        form { display: grid; gap: 12px; }
      </style>
      <form novalidate>
        ${this.#mode === 'create' ? `
        <div class="field">
          <label for="id">ID</label>
          <input id="id" name="id" value="${this.#data.id ?? ''}" />
          <inline-error id="idErr"></inline-error>
        </div>` : ''}
        <div class="field">
          <label for="name">Name</label>
          <input id="name" name="name" value="${this.#data.name ?? ''}" />
          <inline-error id="nameErr"></inline-error>
        </div>
        <div class="field">
          <label for="comments">Comments</label>
          <textarea id="comments" name="comments">${(this.#data.comments ?? '') as string}</textarea>
        </div>
        <div style="display:flex; gap: 8px;">
          <button type="submit" class="btn primary">${this.#mode === 'create' ? 'Create' : 'Save'}</button>
          <button type="button" class="btn ghost" id="cancel">Cancel</button>
        </div>
      </form>
    `;
    const form = this.#root.querySelector('form')!;
    const onBlurValidate = () => this.validate();
    form.querySelectorAll('input,textarea').forEach(el => el.addEventListener('blur', onBlurValidate));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!this.validate()) return;
      const id = (this.#root.querySelector('#id') as HTMLInputElement)?.value?.trim();
      const name = (this.#root.querySelector('#name') as HTMLInputElement).value.trim();
      const comments = (this.#root.querySelector('#comments') as HTMLTextAreaElement).value || undefined;
      const payload: FormData = { id: id || this.#data.id, name, comments };
      this.dispatchEvent(new CustomEvent('submit', { detail: payload }));
    });
    this.#root.querySelector('#cancel')?.addEventListener('click', () => this.dispatchEvent(new Event('cancel')));
  }
}

customElements.define('app-form', AppForm);

