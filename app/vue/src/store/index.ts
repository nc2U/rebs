import { createStore } from 'vuex'
import tagsView from '@/store/modules/tagsView'
import accounts from '@/store/modules/accounts'
import comCash from '@/store/modules/comCash'
import contract from '@/store/modules/contract'
import document from '@/store/modules/document'
import notice from '@/store/modules/notice'
import payment from '@/store/modules/payment'
import project from '@/store/modules/project'
import proCash from '@/store/modules/proCash'
import settings from '@/store/modules/settings'
import Cookies from 'js-cookie'

export interface State {
  [key: string]: any
}

declare interface RootState extends State {
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
  updateState(state: RootState, payload: any) {
    Object.keys(payload).forEach(key => {
      if (state.hasOwnProperty(key)) state[key] = payload[key]
    })
  },
  toggleAside(state: RootState) {
    state.asideVisible = !state.asideVisible
  },
  toggleSidebar(state: RootState) {
    const sidebarVisible = !state.sidebarVisible
    state.sidebarVisible = sidebarVisible
    Cookies.set('sidebarVisible', String(sidebarVisible))
  },
  toggleTheme(state: RootState, payload: any) {
    state.theme = payload.value
    Cookies.set('theme', payload.value)
  },
  toggleUnfoldable(state: RootState) {
    const sidebarUnfoldable = !state.sidebarUnfoldable
    state.sidebarUnfoldable = sidebarUnfoldable
    Cookies.set('sidebarUnfoldable', String(sidebarUnfoldable))
  },
  updateSidebarVisible(state: RootState, payload: any) {
    state.sidebarVisible = payload.value
    Cookies.set('sidebarVisible', payload.value)
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
  modules: {
    tagsView,
    accounts,
    comCash,
    contract,
    document,
    notice,
    payment,
    project,
    proCash,
    settings,
  },
})

export default store
