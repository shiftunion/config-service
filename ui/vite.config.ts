import { defineConfig } from 'vite';

export default defineConfig({
  root: '.',
  server: {
    port: 5173,
    proxy: {
      // Avoid CORS in dev: proxy API to backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
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
