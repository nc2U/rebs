import {defineConfig} from "vitepress";

export default defineConfig({
  lang: 'ko-KR',
  title: 'REBS',
  description: '부동산 개발관리 프로그램',
  base: '/docs/',
  lastUpdated: true,
  // outDir: '../../django/templates/docs',
  markdown: {
    theme: 'material-palenight',
    lineNumbers: true
  },
  themeConfig: {
    // Type is `DefaultTheme.Config`
    logo: '/favicon.png',
    siteTitle: 'REBS',
    nav: [
      {text: '가이드', link: '/getting-started'},
      // {
      //   text: 'Dropdown Menu',
      //   items: [
      //     {text: 'Item A', link: '/item-1'},
      //     {text: 'Item B', link: '/item-2'},
      //     {text: 'Item C', link: '/item-3'}
      //   ]
      // }
    ],
    sidebar: [
      {
        text: '소개',
        items: [
          {text: 'REBS란?', link: '/'},
          {text: '시작하기', link: '/getting-started'},
          {text: '회사설정', link: '/company'},
          {text: '프로젝트 설정', link: '/project'},
          {text: '계약등록', link: '/contract'},
          {text: '입출금 관리', link: '/cash-inout'},
        ]
      }
    ],
    socialLinks: [
      {icon: 'github', link: 'https://github.com/vuejs/vitepress'},
      {icon: 'slack', link: '...'},
    ],
    editLink: {
      pattern: 'https://github.com/vuejs/vitepress/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
    carbonAds: {
      code: 'your-carbon-code',
      placement: 'your-carbon-placement'
    },
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2019-present REBS'
    },
  }
})
