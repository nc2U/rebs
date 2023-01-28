<script lang="ts" setup>
import { ref } from 'vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const msg = ref('현장 문서관리')
</script>

<template>
  <ContentHeader
    :page-title="'현장 문서관리'"
    :nav-menu="['현장 일반문서']"
    :selector="'ProjectSelect'"
  />
  <ContentBody>
    <CCardBody>
      {{ msg }}<br />
      <a href="/rebs/docs/project/general/" target="_blank">
        구) 현장 일반 문서 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
