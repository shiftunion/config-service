import { describe, it, expect } from 'vitest';
import '../../src/components/app-form/app-form';

describe('app-form', () => {
  it('emits submit with values when valid', () => {
    const el = document.createElement('app-form') as any;
    document.body.appendChild(el);
    el.data = { id: '', name: 'Alpha', comments: 'c' };
    const submitted = new Promise(resolve => el.addEventListener('submit', (e: any) => resolve(e.detail)));
    const name = el.shadowRoot!.querySelector('#name') as HTMLInputElement;
    name.value = 'Alpha';
    const id = el.shadowRoot!.querySelector('#id') as HTMLInputElement;
    id.value = 'alpha';
    (el.shadowRoot!.querySelector('form') as HTMLFormElement).dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    return submitted.then((detail: any) => {
      expect(detail.name).toBe('Alpha');
      expect(detail.id).toBe('alpha');
    });
  });
});

