import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import router from "./router";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import VueSidebarMenu from "vue-sidebar-menu";
import "vue-sidebar-menu/dist/vue-sidebar-menu.css";
/* import font awesome icon component */
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
/* import the fontawesome core */
import { library } from "@fortawesome/fontawesome-svg-core";
/* import specific icons */
import { faUserSecret } from "@fortawesome/free-solid-svg-icons";
/* add icons to the library */
library.add(faUserSecret);

loadFonts().then(() => {
  const app = createApp(App);
  app.component("font-awesome-icon", FontAwesomeIcon);
  app.use(router).use(store).use(vuetify).use(VueSidebarMenu);
  app.mount("#app");
});
