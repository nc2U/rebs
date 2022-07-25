import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import DefaultLayout from "@/Layouts/DefaultLayout.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "Home",
    component: DefaultLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: () => import("@/views/HomeView.vue"),
      },
      {
        path: "/charts",
        name: "charts",
        children: [
          {
            path: "sublink1",
            name: "sublink1",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink2",
            name: "sublink2",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink3",
            name: "sublink3",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink4",
            name: "sublink4",
            component: () => import("@/views/AboutView.vue"),
          },
        ],
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
