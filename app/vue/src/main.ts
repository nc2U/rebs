import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import VueSidebarMenu from "vue-sidebar-menu";
import "vue-sidebar-menu/dist/vue-sidebar-menu.css";

loadFonts().then(() => {
  const app = createApp(App);
  app.use(router).use(store).use(vuetify).use(VueSidebarMenu);
  app.mount("#app");
});
