import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import copy from 'rollup-plugin-copy'

import path = require('path')

// https://vitejs.dev/config/
export default defineConfig({
  base:
    process.env.NODE_ENV === 'production'
      ? '/static/dist/'
      : 'http://localhost:3000',
  build: {
    outDir: '../django/static/dist',
    emptyOutDir: true,
    chunkSizeWarningLimit: 1010,
    rollupOptions: {
      plugins: [
        copy({
          targets: [
            {
              src: '../django/static/dist/index.html',
              dest: '../django/templates',
              rename: 'base-vue.html',
            },
          ],
        }),
      ],
    },
  },
  plugins: [
    vue(),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost',
        changeOrigin: true,
      },
    },
  },
})
