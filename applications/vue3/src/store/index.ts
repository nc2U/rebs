import { createStore } from 'vuex'
import accounts from '@/store/modules/accounts'
import contract from '@/store/modules/contract'
import project from '@/store/modules/project'
import project_cash from '@/store/modules/project_cash'
import cash from '@/store/modules/cash'
import settings from '@/store/modules/settings'

declare interface RootState {
  asideVisible: boolean
  sidebarVisible: boolean
  sidebarUnfoldable: boolean
  theme: string
}

const state: RootState = {
  asideVisible: false,
  sidebarVisible: true,
  sidebarUnfoldable: false,
  theme: 'default',
}

const mutations = {
  toggleAside(state: any) {
    state.asideVisible = !state.asideVisible
  },
  toggleSidebar(state: any) {
    state.sidebarVisible = !state.sidebarVisible
  },
  toggleTheme(state: any, payload: any) {
    state.theme = payload.value
  },
  toggleUnfoldable(state: any) {
    state.sidebarUnfoldable = !state.sidebarUnfoldable
  },
  updateSidebarVisible(state: any, payload: any) {
    state.sidebarVisible = payload.value
  },
}

const store: any = createStore({
  state,
  mutations,
  modules: {
    accounts,
    contract,
    project,
    project_cash,
    cash,
    settings,
  },
})

export default store
