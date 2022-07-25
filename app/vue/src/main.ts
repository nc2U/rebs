import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";

loadFonts().then(() => {
  const app = createApp(App);
  app.use(router).use(store).use(vuetify);
  app.mount("#app");
});
