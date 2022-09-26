<script setup lang="ts">
import { reactive, computed, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useDocument, PostFilter } from '@/store/pinia/document'
import { AFile, Attatches, Link, PatchPost, Post } from '@/store/types/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'
import DocsView from './components/DocsView.vue'
import DocsForm from './components/DocsForm.vue'

const postFilter = reactive<PostFilter>({
  board: 1,
  category: null,
  is_com: false,
  project: '',
  ordering: '',
  search: '',
})

const docsFilter = (payload: PostFilter) => {
  postFilter.is_com = payload.is_com
  if (!payload.is_com) postFilter.project = payload.project
  postFilter.ordering = payload.ordering
  postFilter.search = payload.search
  fetchPostList({ ...postFilter })
}

const selectCate = (cate: number) => {
  postFilter.category = cate
  docsFilter(postFilter)
}
const pageSelect = (page: number) => console.log(page)

const documentStore = useDocument()
const postList = computed(() => documentStore.postList)
const categoryList = computed(() => documentStore.categoryList)

const fetchPostList = (payload: PostFilter) =>
  documentStore.fetchPostList(payload)
const fetchCategoryList = (board: number) =>
  documentStore.fetchCategoryList(board)

const createPost = (payload: Post) => documentStore.createPost(payload)
const updatePost = (payload: Post) => documentStore.updatePost(payload)
const patchPost = (payload: PatchPost) => documentStore.patchPost(payload)
const patchLink = (payload: Link) => documentStore.patchLink(payload)
const patchFile = (payload: AFile) => documentStore.patchFile(payload)

const router = useRouter()
const onSubmit = (payload: Post & Attatches) => {
  if (payload.pk) {
    updatePost(payload)
    router.replace({
      name: '본사 일반문서 - 보기',
      params: { postId: payload.pk },
    })
  } else {
    createPost(payload)
    router.replace({ name: '본사 일반문서' })
  }
}

const postHit = (payload: PatchPost) => patchPost(payload)
const linkHit = (payload: Link) => patchLink(payload)
const fileHit = (payload: AFile) => patchFile(payload)

onBeforeMount(() => {
  fetchCategoryList(1)
  fetchPostList({ board: 1 })
})
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="$route.name === '본사 일반문서'" class="pt-3">
        <ListController @docs-filter="docsFilter" />

        <CategoryTabs :category-list="categoryList" @select-cate="selectCate" />

        <DocsList :post-list="postList" @page-select="pageSelect" />
      </div>

      <div v-else-if="$route.name.includes('보기')">
        <DocsView
          :category="postFilter.category"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
        />
      </div>

      <div v-else-if="$route.name.includes('작성')">
        <DocsForm :category-list="categoryList" @on-submit="onSubmit" />
      </div>

      <div v-else-if="$route.name.includes('수정')">
        <DocsForm :category-list="categoryList" @on-submit="onSubmit" />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
