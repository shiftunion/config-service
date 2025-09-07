type Row = { key: string; type: 'string'|'number'|'boolean'|'json'; value: string };

export class ConfigEditor extends HTMLElement {
  #root: ShadowRoot;
  #rows: Row[] = [];
  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
  }

  set value(obj: Record<string, unknown>) {
    this.#rows = Object.entries(obj || {}).map(([k, v]) => {
      const t = typeof v;
      if (t === 'string' || t === 'number' || t === 'boolean') return { key: k, type: t as any, value: String(v) };
      return { key: k, type: 'json', value: JSON.stringify(v) };
    });
    this.render();
  }

  get value(): Record<string, unknown> {
    const out: Record<string, unknown> = {};
    for (const r of this.#rows) {
      if (!r.key) continue;
      let parsed: unknown = r.value;
      if (r.type === 'number') parsed = Number(r.value);
      if (r.type === 'boolean') parsed = r.value === 'true';
      if (r.type === 'json') { try { parsed = JSON.parse(r.value); } catch { parsed = r.value; } }
      out[r.key] = parsed;
    }
    return out;
  }

  connectedCallback() { this.render(); }

  private addRow() { this.#rows = [...this.#rows, { key: '', type: 'string', value: '' }]; this.render(); }
  private removeRow(idx: number) { this.#rows = this.#rows.filter((_, i) => i !== idx); this.render(); }

  render() {
    this.#root.innerHTML = `
      <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { border-bottom: 1px solid var(--border); padding: 8px; }
        tfoot { text-align: right; }
        input, select, textarea { width: 100%; }
        textarea { min-height: 60px; }
      </style>
      <table>
        <thead>
          <tr><th style="width:30%">Key</th><th style="width:20%">Type</th><th>Value</th><th style="width:60px"></th></tr>
        </thead>
        <tbody>
          ${this.#rows.map((r, i) => `
            <tr>
              <td><input data-i="${i}" data-f="key" value="${r.key}" /></td>
              <td>
                <select data-i="${i}" data-f="type" value="${r.type}">
                  ${['string','number','boolean','json'].map(t => `<option value="${t}" ${r.type===t?'selected':''}>${t}</option>`).join('')}
                </select>
              </td>
              <td>${r.type === 'json' ? `<textarea data-i="${i}" data-f="value">${r.value}</textarea>` : `<input data-i="${i}" data-f="value" value="${r.value}" />`}</td>
              <td><button class="btn ghost" data-i="${i}" data-act="del">🗑️</button></td>
            </tr>
          `).join('')}
        </tbody>
        <tfoot>
          <tr><td colspan="4"><button class="btn" data-act="add">Add</button></td></tr>
        </tfoot>
      </table>
    `;
    this.#root.querySelector('[data-act="add"]')?.addEventListener('click', () => this.addRow());
    this.#root.querySelectorAll('[data-act="del"]').forEach(btn => btn.addEventListener('click', () => this.removeRow(parseInt((btn as HTMLElement).dataset.i!, 10))));
    this.#root.querySelectorAll('input,select,textarea').forEach(el => el.addEventListener('input', (e) => {
      const t = e.currentTarget as HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement;
      const i = parseInt(t.dataset.i!, 10);
      const f = t.dataset.f as keyof Row;
      const rows = [...this.#rows];
      (rows[i] as any)[f] = t.value;
      this.#rows = rows;
    }));
  }
}

customElements.define('config-editor', ConfigEditor);

