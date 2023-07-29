import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), VitePWA({
    registerType: 'autoUpdate',
    injectRegister: 'script',
    workbox: {
      globPatterns: ['**/*.{js,css,html,ico,png,svg,json,vue,txt,woff2}'],
        cleanupOutdatedCaches: false
    },
    manifest:{
      name:"Club de barrio villa elisa",
      short_name:"cbve",
      description:"an pwa for Club de Barrio Villa",
      theme_color:"#fafafa",
      background_color:"#fafafa",
      display:"standalone",
      icons: [
        {
            "src": "/android-chrome-36x36.png",
            "sizes": "36x36",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-48x48.png",
            "sizes": "48x48",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-72x72.png",
            "sizes": "72x72",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-96x96.png",
            "sizes": "96x96",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-144x144.png",
            "sizes": "144x144",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-256x256.png",
            "sizes": "256x256",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-384x384.png",
            "sizes": "384x384",
            "type": "image/png"
        },
        {
            "src": "/android-chrome-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
        }
    ]
    }
  })]
})
