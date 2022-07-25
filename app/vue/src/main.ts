import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import mixins from '@/mixins'
import Cookies from 'js-cookie'
import CoreuiVue from '@coreui/vue-pro'
import { CIcon } from '@coreui/icons-vue'
import { iconsSet as icons } from '@/assets/icons'

import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

loadFonts()

import '@/style.css'

function init() {
  const cookedToken = Cookies.get('accessToken')
  if (cookedToken) {
    return store.dispatch('accounts/loginByToken', cookedToken)
  } else {
    return Promise.resolve()
  }
}

init().then(() => {
  const app = createApp(App)
  app.use(store)
  app.use(router)
  app.use(vuetify)
  app.mixin(mixins)
  app.use(CoreuiVue)
  app.provide('icons', icons)
  app.component('CIcon', CIcon)

  app.mount('#app')
})
