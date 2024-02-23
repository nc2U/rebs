<script setup lang="ts">
import { inject, ref } from 'vue'
import { navMenu } from '@/views/_Work/_menu/headermixin1'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const cBody = ref()
const comName = (inject('comStore') as any).company.name

const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      {{ $route.name }}
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
