<script setup lang="ts">
import { defineComponent } from 'vue'
import { navMenu } from '@/views/comDocs/_menu/headermixin'
import HeaderNav from '@/components/HeaderNav.vue'
import ListController from './components/ListController.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <HeaderNav :menus="navMenu" />

      <ListController />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
