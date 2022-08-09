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
      {
        text: 'Dropdown',
        items: [
          {text: 'Item A', link: '/item-1'},
          {text: 'Item B', link: '/item-2'},
          {text: 'Item C', link: '/item-3'}
        ]
      }
    ],
    sidebar: [
      {
        text: '소개',
        items: [
          {text: 'REBS란?', link: '/'},
          {text: '시작하기', link: '/getting-started'},
        ]
      },
      {
        text: '기본 설정',
        items: [
          {text: '회사정보 설정', link: '/company'},
          {text: '프로젝트 설정', link: '/project'},
          {text: '세부정보 설정', link: '/settings'},
          {text: '부지정보 입력', link: '/site-manage'},
        ]
      },
      {
        text: '계약 관리',
        items: [
          {text: '계약 등록 관리', link: '/contract'},
          {text: '계약 해지 관리', link: '/release'},
        ]
      },
      {
        text: '분양대금 수납 관리',
        items: [
          {text: '수납 등록 관리', link: '/payment'},
          {text: '고지서 발급 관리', link: '/bill-notice'},
        ]
      },
      {
        text: '일반 입출금 관리',
        items: [
          {text: '설정 관리', link: '/cash-settings'},
          {text: '입출금 관리', link: '/cash-manage'},
        ]
      },
      {
        text: '권한 관리',
        items: [
          {text: '사용자 권한 관리', link: '/auth-manage'},
          {text: 'admin 페이지', link: '/admin-page'},
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
