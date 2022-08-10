import {defineConfig} from "vitepress";

export default defineConfig({
  lang: 'ko-KR',
  title: 'REBS',
  description: '부동산 개발관리 프로그램',
  base: process.env.NODE_ENV === 'production'
    ? '/rebs/'
    : '',
  head: [
    ['link', {rel: 'shortcut icon', href: '/favicon.png'}]
  ],
  lastUpdated: true,
  markdown: {
    theme: 'material-palenight',
    lineNumbers: true,
  },
  themeConfig: {
    logo: '/favicon.png',
    siteTitle: 'REBS',
    nav: [
      {text: '가이드', link: '/intro/getting-started'},
      {
        text: '관련 사이트',
        items: [
          {text: 'REBS', link: 'https://brdnc.co.kr'},
          {text: 'REBS 구버전', link: 'https://brdnc.co.kr/rebs/'},
          {text: 'API 인덱스', link: 'https://brdnc.co.kr/api/'},
          {text: '관리자 페이지', link: 'https://brdnc.co.kr/admin/'}
        ]
      }
    ],
    sidebar: [
      {
        text: '소개',
        items: [
          {text: 'REBS란?', link: '/'},
          {text: '시작하기', link: '/intro/getting-started'},
        ]
      },
      {
        text: '기본 설정',
        items: [
          {text: '회사정보 설정', link: '/settings/company'},
          {text: '프로젝트 설정', link: '/settings/project'},
          {text: '세부정보 설정', link: '/settings/details'},
          {text: '부지정보 관리', link: '/settings/site-manage'},
        ]
      },
      {
        text: '계약 수납 관리',
        items: [
          {text: '계약 관리', link: '/contract/'},
          {text: '수납 관리', link: '/contract/payment'},
          {text: '고지서 관리', link: '/contract/bill-notice'},
        ]
      },
      {
        text: '일반 입출금 관리',
        items: [
          {text: '기본 설정', link: '/cashes/settings'},
          {text: '입출금 관리', link: '/cashes/manage'},
        ]
      },
      {
        text: '문서 관리',
        items: [
          {text: '일반 문서', link: '/document/'},
          {text: '소송 기록', link: '/document/legal-case'},
        ]
      },
      {
        text: '권한 관리',
        items: [
          {text: '사용자 권한', link: '/authority/'},
          {text: '관리자 페이지', link: '/authority/admin-page'},
        ]
      }
    ],
    socialLinks: [
      {icon: 'github', link: 'https://github.com/nc2U/Rebs'},
      {icon: 'slack', link: 'https://br-on.slack.com'},
    ],
    editLink: {
      pattern: 'https://github.com/nc2U/Rebs/blob/master/app/vue/docs/:path',
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
