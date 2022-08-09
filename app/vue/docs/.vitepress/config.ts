import {defineConfig} from "vitepress";

export default defineConfig({
  lang: 'ko-KR',
  title: 'REBS',
  description: '부동산 개발관리 프로그램',
  base: '/docs/',
  lastUpdated: true,
  markdown: {
    theme: 'material-palenight',
    lineNumbers: true
  },
  themeConfig: {
    // Type is `DefaultTheme.Config`
  }
})
