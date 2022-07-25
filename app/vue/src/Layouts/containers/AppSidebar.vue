<script lang="ts" setup>
import { ref } from "vue";

const menu = ref([
  {
    header: "Main Navigation",
    hiddenOnCollapse: true,
  },
  {
    href: "/",
    title: "Dashboard1",
    icon: "fa-solid fa-coffee",
  },
  {
    href: "/charts",
    title: "Charts",
    icon: "fa-solid fa-coffee",
    child: [
      {
        href: "/charts/sublink1",
        title: "Sub Link1",
      },
      {
        href: "/charts/sublink2",
        title: "Sub Link2",
      },
      {
        href: "/charts/sublink3",
        title: "Sub Link3",
      },
      {
        href: "/charts/sublink4",
        title: "Sub Link4",
      },
    ],
  },
]);
const onToggleCollapse = (collapsed: boolean) => !collapsed;
const onItemClick = (event: Event, item: any) => item;
</script>

<template>
  <SidebarMenu
    :menu="menu"
    width="260px"
    width-collapsed="65px"
    :show-one-child="true"
    :show-child="false"
    :relative="true"
    :hide-toggle="false"
    :disable-hover="true"
    @update:collapsed="onToggleCollapse"
    @item-click="onItemClick"
  />
</template>
