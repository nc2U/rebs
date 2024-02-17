<script setup lang="ts">
import { pageTitle, navMenu } from '@/views/_WorkManage/_menu/headermixin20'
import Header from '../_pubComp/Header/Index.vue'
import Body from '../_pubComp/Body/Index.vue'
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" />

  <Body />
</template>
