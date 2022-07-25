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
        name: "메인 페이지",
        // route level code-splitting
        // this generates a separate chunk (dashboard.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
          import(/* webpackChunkName: "dashboard" */ "@/views/HomeView.vue"),
      },
      {
        path: "/charts",
        name: "charts",
        redirect: "/charts/sublink1",
        children: [
          {
            path: "sublink1",
            name: "charts1",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink2",
            name: "charts2",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink3",
            name: "charts3",
            component: () => import("@/views/AboutView.vue"),
          },
          {
            path: "sublink4",
            name: "charts4",
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
