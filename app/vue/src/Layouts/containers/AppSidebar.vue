<script lang="ts" setup>
import { ref } from "vue";

const menu = ref([
  {
    header: "Main Navigation",
    hiddenOnCollapse: true,
  },
  {
    href: "/",
    title: "Dashboard",
    icon: "fa fa-user",
  },
  {
    href: "/charts",
    title: "Charts",
    icon: "fa fa-chart-area",
    child: [
      {
        href: "/charts/sublink",
        title: "Sub Link",
      },
    ],
  },
]);
const onToggleCollapse = (collapsed: boolean) => !collapsed;
const onItemClick = (event: Event, item: any) => (event.target.value, item);
</script>

<template>
  <SidebarMenu
    :menu="menu"
    width="290px"
    width-collapsed="65px"
    :show-one-child="true"
    :show-child="true"
    :relative="true"
    :hide-toggle="false"
    :disable-hover="true"
    @update:collapsed="onToggleCollapse"
    @item-click="onItemClick"
  />
</template>
