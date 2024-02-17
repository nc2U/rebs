<script setup lang="ts">
import { pageTitle, navMenu } from '@/views/_WorkManage/_menu/headermixin12'
import Header from '../_pubComp/Header/Index.vue'
import ContentBody from '@/views/_WorkManage/_pubComp/ContentBody/Index.vue'
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody></ContentBody>
</template>
