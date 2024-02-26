<script setup lang="ts">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default> {{ $route.name }} ==</template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
