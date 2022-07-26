import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { baseUrl } from 'rollup-plugin-base-url'
import copy from 'rollup-plugin-copy-merge'

const path = require('path')

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        dir: '../django/static/dist',
      },
    },
  },
  plugins: [
    vue(),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
    baseUrl({
      url: '/static/dist',
      // the base URL prefix; optional, defaults to /
      // staticImports: true,
      // also rebases static `import _ from "…"`; optional, defaults to false
    }),
    copy({
      targets: [
        {
          src: '../django/static/dist/index.html',
          file: '../django/templates/base-vue.html',
        },
      ],
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  /* remove the need to specify .vue files https://vitejs.dev/config/#resolve-extensions
  resolve: {
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ]
  },
  */
})
