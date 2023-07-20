import { createApp } from 'vue'
import { useAccount } from '@/store/pinia/account'
import { loadFonts } from './plugins/webfontloader'
import { CIcon } from '@coreui/icons-vue'
import { iconsSet as icons } from '@/assets/icons'
import { vMaska } from 'maska'
import store, { pinia } from './store'
import router from './router'
import Cookies from 'js-cookie'
import CoreuiVue from '@coreui/vue'
import vuetify from './plugins/vuetify'
import '@/styles/style.scss'
import App from './App.vue'

const app = createApp(App)
app.use(pinia)
const account = useAccount()
const cookie = Cookies.get('accessToken')
const init = () => account.loginByToken(cookie)

init().then(() => {
  loadFonts().then(() => {
    app.use(store)
    app.use(router)
    app.use(vuetify)
    app.use(CoreuiVue, [])
    app.provide('icons', icons)
    app.component('CIcon', CIcon)
    app.directive('maska', vMaska)
    app.mount('#app')
  })
})
