type Column<T> = { key: keyof T & string; header: string; width?: string };

export class AppTable<T extends Record<string, any>> extends HTMLElement {
  #root: ShadowRoot;
  #items: T[] = [];
  #columns: Column<T>[] = [];
  #page = 1;
  #pageSize = 20;
  #sortKey: string | null = null;
  #sortDir: 'asc' | 'desc' = 'desc';

  constructor() {
    super();
    this.#root = this.attachShadow({ mode: 'open' });
  }

  set items(v: T[]) { this.#items = Array.isArray(v) ? v : []; this.#page = 1; this.render(); }
  set columns(v: Column<T>[]) { this.#columns = v; this.render(); }
  set pageSize(v: number) { this.#pageSize = v > 0 ? v : 20; this.render(); }
  set sort(key: string | null) { this.#sortKey = key; this.render(); }

  connectedCallback() { this.render(); }

  get paged(): T[] {
    let items = [...this.#items];
    if (this.#sortKey) {
      items.sort((a, b) => {
        const av = a[this.#sortKey!];
        const bv = b[this.#sortKey!];
        const r = ('' + av).localeCompare('' + bv);
        return this.#sortDir === 'asc' ? r : -r;
      });
    }
    const start = (this.#page - 1) * this.#pageSize;
    return items.slice(start, start + this.#pageSize);
  }

  render() {
    const total = this.#items.length;
    const pages = Math.max(1, Math.ceil(total / this.#pageSize));
    if (this.#page > pages) this.#page = pages;
    this.#root.innerHTML = `
      <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { border-bottom: 1px solid var(--border); padding: 10px; height: var(--table-row-height); }
        th { text-align: left; color: var(--text-muted); font-weight: 600; }
        tr:hover { background: var(--surface-2); }
        .toolbar { margin-bottom: 12px; }
        .pagination { display: flex; gap: 8px; align-items: center; justify-content: flex-end; padding-top: 8px; }
        button { cursor: pointer; }
        .sortable { cursor: pointer; }
      </style>
      <div class="card">
        <div class="toolbar" part="toolbar">
          <slot name="toolbar"></slot>
        </div>
        <table part="table">
          <thead>
            <tr>
              ${this.#columns.map(c => `<th style="width:${c.width ?? 'auto'}">
                <span class="sortable" data-key="${c.key}">${c.header}${this.#sortKey === c.key ? (this.#sortDir === 'asc' ? ' ▲' : ' ▼') : ''}</span>
              </th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${this.paged.map(row => `<tr data-row="1" data-id="${'id' in row ? row['id'] : ''}">
              ${this.#columns.map(c => `<td>${this.renderCell(row[c.key])}</td>`).join('')}
            </tr>`).join('') || `<tr><td colspan=\"${this.#columns.length}\"><slot name=\"empty\">No data.</slot></td></tr>`}
          </tbody>
        </table>
        <div class="pagination">
          <button class="btn ghost" data-act="prev" ${this.#page <= 1 ? 'disabled' : ''}>Prev</button>
          <span>Page ${this.#page} / ${pages}</span>
          <button class="btn ghost" data-act="next" ${this.#page >= pages ? 'disabled' : ''}>Next</button>
        </div>
      </div>
    `;
    this.#root.querySelectorAll('[data-key]')?.forEach(el => el.addEventListener('click', () => {
      const key = (el as HTMLElement).dataset.key!;
      if (this.#sortKey === key) this.#sortDir = this.#sortDir === 'asc' ? 'desc' : 'asc';
      this.#sortKey = key;
      this.render();
      this.dispatchEvent(new CustomEvent('sort-change', { detail: { key: this.#sortKey, dir: this.#sortDir } }));
    }));
    this.#root.querySelector('[data-act="prev"]')?.addEventListener('click', () => { this.#page = Math.max(1, this.#page - 1); this.render(); });
    this.#root.querySelector('[data-act="next"]')?.addEventListener('click', () => { this.#page += 1; this.render(); });
    this.#root.querySelectorAll('tbody tr[data-row]')?.forEach(tr => tr.addEventListener('click', () => {
      const id = (tr as HTMLElement).dataset.id;
      this.dispatchEvent(new CustomEvent('row-activate', { detail: { id } }));
    }));
  }

  private renderCell(value: unknown): string {
    if (value == null) return '';
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') return String(value);
    return `<code>${escapeHtml(JSON.stringify(value))}</code>`;
  }
}

function escapeHtml(s: string) {
  return s.replace(/[&<>"] /g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', ' ': ' ' } as any)[c]);
}

customElements.define('app-table', AppTable as any);
