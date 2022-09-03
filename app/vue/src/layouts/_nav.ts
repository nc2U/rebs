const dashboard = {
  component: 'CNavItem',
  name: '메인 페이지',
  to: '/dashboard',
  icon: 'cil-speedometer',
  badge: {
    color: 'danger',
    text: 'u.c',
  },
}

const schedule = {
  component: 'CNavItem',
  name: '일 정 관 리',
  to: '/schedule',
  icon: 'cil-calendar',
}

const contract = {
  component: 'CNavItem',
  name: '분양계약 관리',
  to: '/contracts',
  icon: 'cil-spreadsheet',
  items: [
    {
      component: 'CNavItem',
      name: '계약내역 조회',
      to: '/contracts/index',
    },
    {
      component: 'CNavItem',
      name: '계약등록 관리',
      to: '/contracts/register',
    },
    {
      component: 'CNavItem',
      name: '동호수 현황표',
      to: '/contracts/status',
    },
    {
      component: 'CNavItem',
      name: '계약해지 관리',
      to: '/contracts/cancel',
    },
  ],
}

const payment = {
  component: 'CNavItem',
  name: '분양수납 관리',
  to: '/payments',
  icon: 'cil-calculator',
  items: [
    {
      component: 'CNavItem',
      name: '분양수납 내역',
      to: '/payments/index',
    },
    {
      component: 'CNavItem',
      name: '건별수납 관리',
      to: '/payments/manage',
    },
  ],
}

const notice = {
  component: 'CNavItem',
  name: '고객고지 관리',
  to: '/notices',
  icon: 'cil-envelope-letter',
  items: [
    {
      component: 'CNavItem',
      name: '수납고지서 출력',
      to: '/notices/bill',
    },
    {
      component: 'CNavItem',
      name: 'SMS 발송관리',
      to: '/notices/sms',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
    },
    {
      component: 'CNavItem',
      name: 'MAIL 발송관리',
      to: '/notices/mailing',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
    },
    {
      component: 'CNavItem',
      name: '우편라벨 관리',
      to: '/notices/post-label',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
    },
    {
      component: 'CNavItem',
      name: '발송기록 관리',
      to: '/notices/log',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
    },
  ],
}

const project_cash = {
  component: 'CNavItem',
  name: '현장자금 관리',
  to: '/project-cash',
  icon: 'cil-money',
  items: [
    {
      component: 'CNavItem',
      name: '현장자금 현황',
      to: '/project-cash/status',
    },
    {
      component: 'CNavItem',
      name: '현장출납 관리',
      to: '/project-cash/index',
    },
    {
      component: 'CNavItem',
      name: '운영비용 관리',
      to: '/project-cash/imprest',
    },
  ],
}

const project_docs = {
  component: 'CNavItem',
  name: '현장문서 관리',
  to: '/project-docs',
  icon: 'cil-library',
  items: [
    {
      component: 'CNavItem',
      name: '현장 일반문서',
      badge: {
        color: 'warning',
        text: 'link',
      },
      to: '/project-docs/general/docs',
      icon: 'cil-layers',
    },
    {
      component: 'CNavItem',
      name: '현장 소송관리',
      to: '/project-docs/lawsuit',
      icon: 'cil-library-building',
      items: [
        {
          component: 'CNavItem',
          name: '현장 소송문서',
          badge: {
            color: 'warning',
            text: 'link',
          },
          to: '/project-docs/lawsuit/docs',
        },
        {
          component: 'CNavItem',
          name: '현장 소송사건',
          badge: {
            color: 'warning',
            text: 'link',
          },
          to: '/project-docs/lawsuit/case',
        },
      ],
    },
  ],
}

const project = {
  component: 'CNavItem',
  name: '신규 프로젝트',
  to: '/project',
  icon: 'cil-building',
  items: [
    {
      component: 'CNavItem',
      name: '프로젝트 관리',
      to: '/project/manage',
      icon: 'cilStorage',
      items: [
        {
          component: 'CNavItem',
          name: '프로젝트 등록',
          to: '/project/manage/index',
        },
        {
          component: 'CNavItem',
          name: '차수분류 등록',
          to: '/project/manage/order',
        },
        {
          component: 'CNavItem',
          name: '타입정보 등록',
          to: '/project/manage/type',
        },
        {
          component: 'CNavItem',
          name: '층별조건 등록',
          to: '/project/manage/floor',
        },
      ],
    },
    {
      component: 'CNavItem',
      name: '세부설정 관리',
      to: '/project/settings',
      icon: 'cil-cog',
      items: [
        {
          component: 'CNavItem',
          name: '동(건물) 등록',
          to: '/project/settings/bldg',
        },
        {
          component: 'CNavItem',
          name: '호(유닛) 등록',
          to: '/project/settings/unit',
        },
        {
          component: 'CNavItem',
          name: '공급가격 등록',
          to: '/project/settings/price',
        },
        {
          component: 'CNavItem',
          name: '납부회차 등록',
          to: '/project/settings/payment-order',
        },
        {
          component: 'CNavItem',
          name: '계약조건 등록',
          to: '/project/settings/down-payment',
        },
      ],
    },
    {
      component: 'CNavItem',
      name: '사업부지 관리',
      to: '/project/site',
      icon: 'cil-location-pin',
      items: [
        {
          component: 'CNavItem',
          name: '지번목록 관리',
          to: '/project/site/index',
        },
        {
          component: 'CNavItem',
          name: '소유자별 관리',
          to: '/project/site/owner',
        },
        {
          component: 'CNavItem',
          name: '매입계약 관리',
          to: '/project/site/contract',
        },
      ],
    },
  ],
}

const company_cash = {
  component: 'CNavItem',
  name: '본사회계 관리',
  to: '/cashes',
  icon: 'cil-laptop',
  items: [
    {
      component: 'CNavItem',
      name: '본사자금 현황',
      to: '/cashes/status',
    },
    {
      component: 'CNavItem',
      name: '본사출납 관리',
      to: '/cashes/index',
    },
  ],
}

const company_docs = {
  component: 'CNavItem',
  name: '본사문서 관리',
  to: '/docs/general',
  icon: 'cil-cloud-download',
  items: [
    {
      component: 'CNavItem',
      name: '본사 일반문서',
      badge: {
        color: 'warning',
        text: 'link',
      },
      to: '/docs/general/docs',
    },
    {
      component: 'CNavItem',
      name: '본사 소송관리',
      to: '/docs/lawsuit',
      icon: 'cil-library-building',
      items: [
        {
          component: 'CNavItem',
          name: '본사 소송문서',
          badge: {
            color: 'warning',
            text: 'link',
          },
          to: '/docs/lawsuit/docs',
        },
        {
          component: 'CNavItem',
          name: '본사 소송사건',
          badge: {
            color: 'warning',
            text: 'link',
          },
          to: '/docs/lawsuit/case',
        },
      ],
    },
  ],
}

const human_resource = {
  component: 'CNavItem',
  name: '본사인사 관리',
  to: '/hr-manage',
  icon: 'cil-user-follow',
  items: [
    {
      component: 'CNavItem',
      name: '직원정보 관리',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
      to: '/hr-manage/employee',
    },
    {
      component: 'CNavItem',
      name: '부서정보 관리',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
      to: '/hr-manage/department',
    },
    // {
    //   name: '직급정보 관리',
    //   to: '/hr/rank'
    // }
  ],
}

const settings = {
  component: 'CNavItem',
  name: '환 경 설 정',
  to: '/settings',
  icon: 'cil-settings',
  items: [
    {
      component: 'CNavItem',
      name: '회사정보 관리',
      to: '/settings/company',
    },
    {
      component: 'CNavItem',
      name: '권한설정 관리',
      badge: {
        color: 'danger',
        text: 'u.c',
      },
      to: '/settings/authorization',
    },
    {
      component: 'CNavItem',
      name: '프로필 관리',
      to: '/settings/profile',
    },
  ],
}

const nav: any = [
  dashboard,
  schedule,
  {
    component: 'CNavTitle',
    name: '프로젝트 관리',
  },
  contract,
  payment,
  notice,
  project_cash,
  project_docs,
  project,
  {
    component: 'CNavTitle',
    name: '본사 관리',
  },
  company_cash,
  company_docs,
  human_resource,
  {
    component: 'CNavTitle',
    name: '기타 관리',
  },
  settings,
]

export default nav
