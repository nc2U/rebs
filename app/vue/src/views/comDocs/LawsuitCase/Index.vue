<script setup lang="ts">
import { defineComponent } from 'vue'
import { navMenu } from '@/views/comDocs/_menu/headermixin'
import HeaderNav from '@/components/HeaderNav.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <HeaderNav :menus="navMenu" />

      <a href="/rebs/docs/lawsuit/case/" target="_blank">
        구) 소송 사건 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
