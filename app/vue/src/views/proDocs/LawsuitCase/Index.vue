<script lang="ts" setup>
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/proDocs/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const msg = ref('')
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />
  <ContentBody>
    <CCardBody>
      {{ msg }}
      <a href="/rebs/docs/project/lawsuit/case/" target="_blank">
        구) 현장 소송 사건 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
