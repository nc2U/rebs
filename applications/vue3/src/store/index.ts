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
  LoadingStatus: boolean
}

const state: RootState = {
  asideVisible: false,
  sidebarVisible: true,
  sidebarUnfoldable: false,
  theme: 'default',
  LoadingStatus: false,
}

const mutations = {
  toggleAside(state: RootState) {
    state.asideVisible = !state.asideVisible
  },
  toggleSidebar(state: RootState) {
    state.sidebarVisible = !state.sidebarVisible
  },
  toggleTheme(state: RootState, payload: any) {
    state.theme = payload.value
  },
  toggleUnfoldable(state: RootState) {
    state.sidebarUnfoldable = !state.sidebarUnfoldable
  },
  updateSidebarVisible(state: RootState, payload: any) {
    state.sidebarVisible = payload.value
  },
  startSpinner(state: RootState) {
    state.LoadingStatus = true
  },
  endSpinner(state: RootState) {
    state.LoadingStatus = false
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
