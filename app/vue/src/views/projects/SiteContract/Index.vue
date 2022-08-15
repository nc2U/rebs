<script lang="ts" setup>
import { computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <a href="/rebs/project/site-contract/" target="_blank">
        구) 사업부지 - 매매계약 관리 페이지 바로가기
      </a>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
