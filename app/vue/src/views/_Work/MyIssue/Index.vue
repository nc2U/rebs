<script setup lang="ts">
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin11'
import Header from '../components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody />
</template>
