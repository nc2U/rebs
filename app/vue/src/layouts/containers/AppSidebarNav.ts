import { defineComponent, h, ref, resolveComponent, computed } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { RouterLink, useRoute, type RouteLocation } from 'vue-router'

import { CBadge, CNavGroup, CNavItem, CSidebarNav, CNavTitle } from '@coreui/vue'
import { CIcon } from '@coreui/icons-vue'
import nav from '@/layouts/_nav'

type Badge = {
  color?: string
  text?: string
}

type Item = {
  badge?: Badge
  component: string
  icon?: string
  items?: Item[]
  name?: string
  to?: string
}

const workManager = computed(() => useAccount().workManager)
const isStaff = computed(() => useAccount().isStaff)
const isComCash = computed(() => useAccount().isComCash)

const normalizePath = (path: string) =>
  decodeURI(path)
    .replace(/#.*$/, '')
    .replace(/(index)?\.(html)$/, '')

const isActiveLink = (route: RouteLocation, link: string) => {
  if (link === undefined) return false

  if (route.hash === link) return true

  const currentPath = normalizePath(route.path)
  const targetPath = normalizePath(link)

  return currentPath === targetPath
}

const isActiveItem = (route: RouteLocation, item: Item): boolean => {
  if (item.to && isActiveLink(route, item.to)) return true

  if (item.items) return item.items.some(child => isActiveItem(route, child))

  if (item.name && route.meta.title) return item.name === route.meta.title

  return false
}

const AppSidebarNav = defineComponent({
  name: 'AppSidebarNav',
  components: {
    CNavItem,
    CNavGroup,
    CNavTitle,
  },
  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  setup: function () {
    const route = useRoute()
    const firstRender = ref(true)

    const renderItem = (item: Item) => {
      if (item.items) {
        return h(
          CNavGroup,
          {
            ...(firstRender.value && {
              visible: item.items.some(child => isActiveItem(route, child)),
            }),
          },
          {
            togglerContent: () => [
              h(CIcon, {
                customClassName: 'nav-icon',
                name: item.icon,
              }),
              item.name,
            ],
            default: () => item.items && item.items.map(child => renderItem(child)),
          },
        )
      }

      return item.to
        ? h(
            RouterLink,
            {
              to: item.to,
              custom: true,
            },
            {
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              default: (props: any) =>
                h(
                  resolveComponent(item.component),
                  {
                    active: props.isActive,
                    href: props.href,
                    onClick: () => props.navigate(),
                  },
                  () => [
                    item.icon &&
                      h(CIcon, {
                        customClassName: 'nav-icon',
                        name: item.icon,
                      }),
                    item.name,
                    item.badge &&
                      h(
                        CBadge,
                        {
                          class: 'ms-auto',
                          color: item.badge.color,
                        },
                        () => item.badge && item.badge.text,
                      ),
                  ],
                ),
            },
          )
        : h(resolveComponent(item.component), {}, () => item.name)
    }

    const wmPos = 2 // 업무 설정관리 위치
    const coPos = workManager.value ? 3 : 2 // 본사 관리 위치
    const coNum = 1 + 3 // 본사관리 메뉴 개수
    const caPos = coPos + 1 // 본사자금 메뉴 위치

    if (!workManager.value) nav.splice(wmPos, 1) // 업무 설정 관리 메뉴 제외

    if (!isStaff.value) {
      // 본사 관리 직원 권한이 없으면
      nav.splice(coPos, coNum) // 본사 관련 메뉴 제외
    }
    // 본사 자금 관리 권한 없으면 자금 관리 메뉴 제외
    else if (!isComCash.value) nav.splice(caPos, 1)

    return () =>
      h(
        CSidebarNav,
        {},
        {
          default: () => nav.map((item: Item) => renderItem(item)),
        },
      )
  },
})
export { AppSidebarNav }
