import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

/* The game app is served from the .NET host at /spelen/. The build output
   lives inside that project's wwwroot so the old src/ scripts never need to
   be exposed over HTTP again. */
export default defineConfig({
  plugins: [react()],
  base: '/spelen/',
  build: {
    outDir: '../server/Oefenpad.WebUI/wwwroot/spelen',
    emptyOutDir: true
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8098',
      '/assets': 'http://127.0.0.1:8098'
    }
  }
});
