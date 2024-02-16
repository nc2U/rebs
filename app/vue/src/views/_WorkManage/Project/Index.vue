<script setup lang="ts">
import { pageTitle, navMenu } from '@/views/_WorkManage/_menu/headermixin12'
import ContentHeader from '../_common/ContentHeader/Index.vue'
import ContentBody from '../_common/ContentBody/Index.vue'
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody />
</template>
