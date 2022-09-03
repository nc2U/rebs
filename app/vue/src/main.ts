import { createApp } from 'vue'
import { useAccount } from '@/store/pinia/account'
import Cookies from 'js-cookie'
import App from './App.vue'
import store, { pinia } from './store'
import router from './router'
import mixins from '@/mixins/mixins'

import CoreuiVue from '@coreui/vue'
import { CIcon } from '@coreui/icons-vue'
import { iconsSet as icons } from '@/assets/icons'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import '@/styles/style.scss'

function init() {
  const cookedToken = Cookies.get('accessToken')
  return account.loginByToken(cookedToken)
}

const app = createApp(App)
app.use(pinia)
const account = useAccount()
loadFonts().then(() => {
  init().then(() => {
    app.use(store)
    app.use(router)
    app.use(vuetify)
    app.mixin(mixins)
    app.use(CoreuiVue)
    app.provide('icons', icons)
    app.component('CIcon', CIcon)
    app.mount('#app')
  })
})
