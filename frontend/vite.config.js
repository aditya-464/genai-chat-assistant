import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Backend runs on port 5000
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/chat': 'http://localhost:5000'
    }
  }
})
