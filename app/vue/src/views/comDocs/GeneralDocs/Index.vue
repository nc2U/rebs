<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useDocument } from '@/store/pinia/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'

const tab = ref<number>(0)
const documentStore = useDocument()
const fetchCategoryList = (board: number) =>
  documentStore.fetchCategoryList(board)

const onSelectAdd = () => 1

const selectTab = (tabValue: number | null) => (tab.value = tabValue)

onBeforeMount(() => fetchCategoryList(1))
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

      <CategoryTabs @select-tab="selectTab" />

      <DocsList :tab-value="tab" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
