<script setup lang="ts">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_WorkManage/_menu/headermixin12'
import Header from '../_pubComp/Header/Index.vue'
import ContentBody from '@/views/_WorkManage/_pubComp/ContentBody/Index.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>a</template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
