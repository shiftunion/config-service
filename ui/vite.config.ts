import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  server: {
    port: 5173
  },
  build: {
    target: 'es2022',
    outDir: 'dist'
  },
  test: {
    environment: 'happy-dom',
    globals: true
  }
});

