<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useDocument, PostFilter } from '@/store/pinia/document'
// import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'

const tab = ref<number>(0)

const selectTab = (tabValue: number) => (tab.value = tabValue)
const pageSelect = (page: number) => console.log(page)
</script>

<template>
  <!--  <ContentHeader-->
  <!--    :page-title="'본사 문서관리'"-->
  <!--    :nav-menu="['본사 일반문서']"-->
  <!--    :selector="'CompanySelect'"-->
  <!--    @header-select="onSelectAdd"-->
  <!--  />-->
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController />

      <CategoryTabs @select-tab="selectTab" />

      <DocsList :tab-value="tab" @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
