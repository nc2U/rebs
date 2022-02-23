import { createStore } from 'vuex'
import accounts from '@/store/modules/accounts'
import cash from '@/store/modules/cash'
import contract from '@/store/modules/contract'
import document from '@/store/modules/document'
import notice from '@/store/modules/notice'
import payment from '@/store/modules/payment'
import project from '@/store/modules/project'
import project_cash from '@/store/modules/project_cash'
import settings from '@/store/modules/settings'

declare interface RootState {
  asideVisible: boolean
  sidebarVisible: boolean
  sidebarUnfoldable: boolean
  theme: string
  LoadingStatus: boolean
  registerCode: string
}

const state: RootState = {
  asideVisible: false,
  sidebarVisible: true,
  sidebarUnfoldable: false,
  theme: 'default',
  LoadingStatus: false,
  registerCode: 'brdnc00',
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
    cash,
    contract,
    document,
    notice,
    payment,
    project,
    project_cash,
    settings,
  },
})

export default store
