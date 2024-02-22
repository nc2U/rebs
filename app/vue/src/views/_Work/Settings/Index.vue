<script setup lang="ts">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin2'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default> Under Construction!</template>

    <template v-slot:aside> Under Construction!</template>
  </ContentBody>
</template>
