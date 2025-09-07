type Handler = (params: Record<string, string>) => void;

export class Router {
  private routes: { pattern: RegExp; keys: string[]; handler: Handler }[] = [];
  private onNotFound: () => void = () => {};

  add(path: string, handler: Handler) {
    const { pattern, keys } = toRegex(path);
    this.routes.push({ pattern, keys, handler });
    return this;
  }
  notFound(fn: () => void) { this.onNotFound = fn; return this; }
  start() {
    window.addEventListener('hashchange', () => this.resolve());
    this.resolve();
  }
  navigate(path: string) { location.hash = path; }
  resolve() {
    const hash = location.hash.replace(/^#/, '') || '/applications';
    for (const r of this.routes) {
      const m = r.pattern.exec(hash);
      if (m) {
        const params: Record<string, string> = {};
        r.keys.forEach((k, i) => params[k] = decodeURIComponent(m[i + 1] ?? ''));
        r.handler(params);
        return;
      }
    }
    this.onNotFound();
  }
}

function toRegex(path: string): { pattern: RegExp; keys: string[] } {
  const keys: string[] = [];
  const regex = path
    .replace(/\//g, '\\/')
    .replace(/:(\w+)/g, (_, k) => { keys.push(k); return '([^/]+)'; });
  return { pattern: new RegExp('^' + regex + '$'), keys };
}

