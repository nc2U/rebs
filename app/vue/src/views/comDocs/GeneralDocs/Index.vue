<script setup lang="ts">
import { computed, onBeforeMount, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useDocument } from '@/store/pinia/document'
import { PatchPost, Post } from '@/store/types/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'
import DocsView from './components/DocsView.vue'
import DocsForm from './components/DocsForm.vue'

const tab = ref<number>(0)

const documentStore = useDocument()
const post = computed(() => documentStore.post)
const categoryList = computed(() => documentStore.categoryList)

const fetchCategoryList = (board: number) =>
  documentStore.fetchCategoryList(board)

const fetchPost = (pk: number) => documentStore.fetchPost(pk)

const createPost = (payload: Post) => documentStore.createPost(payload)
const updatePost = (payload: Post) => documentStore.updatePost(payload)
const patchPost = (payload: PatchPost) => documentStore.patchPost(payload)

const onSubmit = (payload: Post) => {
  if (payload.pk) console.log(payload) // createPost(payload)
  else return console.log(payload) // updatePost(payload)
}

const hitPlus = (payload: PatchPost) => patchPost(payload)

const selectTab = (tabValue: number) => (tab.value = tabValue)
const pageSelect = (page: number) => console.log(page)

const route = useRoute()

onBeforeMount(() => {
  fetchCategoryList(1)
  if (route.params.postId) fetchPost(Number(route.params.postId))
})
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <CContainer v-if="$route.name === '본사 일반문서'">
        <ListController />

        <CategoryTabs :category-list="categoryList" @select-tab="selectTab" />

        <DocsList :tab-value="tab" @page-select="pageSelect" />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('보기')">
        <DocsView :post="post" @hit-plus="hitPlus" />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('작성')">
        <DocsForm :category-list="categoryList" @on-submit="onSubmit" />
      </CContainer>

      <CContainer v-else-if="$route.name.includes('수정')">
        <DocsForm
          :category-list="categoryList"
          :post="post"
          @on-submit="onSubmit"
        />
      </CContainer>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
