<script setup lang="ts">
import { ref } from 'vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'
import DocsView from './components/DocsView.vue'
import DocsForm from './components/DocsForm.vue'

const tab = ref<number>(0)

const selectTab = (tabValue: number) => (tab.value = tabValue)
const pageSelect = (page: number) => console.log(page)
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <CContainer v-if="$route.name === '본사 일반문서'">
        <ListController />

        <CategoryTabs @select-tab="selectTab" />

        <DocsList :tab-value="tab" @page-select="pageSelect" />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('보기')">
        <DocsView />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('작성')">
        <DocsForm />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('수정')">
        <DocsForm />
      </CContainer>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
