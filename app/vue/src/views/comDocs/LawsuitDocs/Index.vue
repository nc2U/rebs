<script setup lang="ts">
import { computed, onBeforeMount, reactive } from 'vue'
import { navMenu } from '@/views/comDocs/_menu/headermixin'
import { PostFilter, useDocument } from '@/store/pinia/document'
import HeaderNav from '@/components/HeaderNav.vue'
import ListController from './components/ListController.vue'
import DocsList from './components/DocsList.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'

const caseFilter = reactive<PostFilter>({
  board: 2,
  category: null,
  is_com: false,
  project: '',
  ordering: '',
  search: '',
})

const caseFiltering = (payload: PostFilter) => 1

const pageSelect = (page: number) => console.log(page)

const documentStore = useDocument()
const postList = computed(() => documentStore.postList)

const fetchPostList = (payload: PostFilter) =>
  documentStore.fetchPostList(payload)

onBeforeMount(() => {
  fetchPostList({ board: 2 })
})
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <HeaderNav :menus="navMenu" />

      <ListController />

      <DocsList :post-list="postList" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
