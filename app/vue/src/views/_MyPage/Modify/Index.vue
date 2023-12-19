<script lang="ts" setup="">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_MyPage/_menu/headermixin'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" selector="CompanySelect" />

  <ContentBody>
    <CCardBody> a</CCardBody>
  </ContentBody>
</template>
