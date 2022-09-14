<script setup lang="ts">
import { ref } from 'vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'

const msg = ref('')

const onSelectAdd = () => 1
</script>

<template>
  <ContentHeader
    :page-title="'본사 문서관리'"
    :nav-menu="['본사 일반문서']"
    :selector="'CompanySelect'"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController />

      <CategoryTabs />

      <DocsList />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
