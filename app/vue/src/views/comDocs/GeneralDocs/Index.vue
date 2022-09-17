<script setup lang="ts">
import { ref } from 'vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'
import DocsView from './components/DocsView.vue'

const tab = ref<number>(0)

const selectTab = (tabValue: number) => (tab.value = tabValue)
const pageSelect = (page: number) => console.log(page)
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <ListController />

      <CContainer v-if="!$route.params.postId">
        <CategoryTabs @select-tab="selectTab" />

        <DocsList :tab-value="tab" @page-select="pageSelect" />
      </CContainer>

      <CContainer v-else>
        <DocsView />
      </CContainer>
      {{ $router.currentRoute.value.matched }}
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
