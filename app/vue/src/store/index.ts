import { createPinia } from 'pinia'
import { createStore } from 'vuex'
import Cookies from 'js-cookie'

export const pinia = createPinia()

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
  sidebarVisible:
    !Cookies.get('sidebarVisible') || Cookies.get('sidebarVisible') === 'true',
  sidebarUnfoldable: Cookies.get('sidebarUnfoldable') === 'true',
  theme: Cookies.get('theme') || 'default',
  LoadingStatus: false,
  registerCode: 'brdnc00',
}

const mutations = {
  toggleAside(state: RootState) {
    state.asideVisible = !state.asideVisible
  },
  toggleSidebar(state: RootState) {
    const sidebarVisible = !state.sidebarVisible
    state.sidebarVisible = sidebarVisible
    Cookies.set('sidebarVisible', String(sidebarVisible))
  },
  toggleTheme(state: RootState, payload: { value: 'default' | 'dark' }) {
    state.theme = payload.value
    Cookies.set('theme', payload.value)
  },
  toggleUnfoldable(state: RootState) {
    const sidebarUnfoldable = !state.sidebarUnfoldable
    state.sidebarUnfoldable = sidebarUnfoldable
    Cookies.set('sidebarUnfoldable', String(sidebarUnfoldable))
  },
  updateSidebarVisible(state: RootState, payload: { value: boolean }) {
    state.sidebarVisible = payload.value
    Cookies.set('sidebarVisible', String(payload.value))
  },
  startSpinner(state: RootState) {
    state.LoadingStatus = true
  },
  endSpinner(state: RootState) {
    state.LoadingStatus = false
  },
}

const store = createStore({
  state,
  mutations,
})

export default store
