import { describe, it, expect } from 'vitest';
import '../../src/components/config-editor/config-editor';

describe('config-editor', () => {
  it('round-trips values', () => {
    const el = document.createElement('config-editor') as any;
    document.body.appendChild(el);
    el.value = { a: '1', b: 2, c: true, d: { e: 1 } };
    const val = el.value;
    expect(val.a).toBe('1');
    expect(val.b).toBe(2);
    expect(val.c).toBe(true);
    expect((val.d as any).e).toBe(1);
  });
});

