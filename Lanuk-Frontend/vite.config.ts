import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
// export default defineConfig({
 // plugins: [react()], })


export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist', 
    emptyOutDir: true, 
  },
  // Development server settings (only used in dev mode)
  server: {
    host: true, 
    port: 5173, 
  },
})
