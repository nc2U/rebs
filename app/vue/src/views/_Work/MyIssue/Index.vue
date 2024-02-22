<script setup lang="ts">
import { ref } from 'vue'
import { pageTitle } from '@/views/_Work/_menu/headermixin1'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :query="$route?.query">
    <template v-slot:default></template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
