<script setup lang="ts">
import { computed, onBeforeMount, onBeforeUpdate, reactive } from 'vue'
import { navMenu } from '@/views/comDocs/_menu/headermixin'
import { useRouter } from 'vue-router'
import { PostFilter, useDocument } from '@/store/pinia/document'
import { AFile, Attatches, Link, PatchPost, Post } from '@/store/types/document'
import HeaderNav from '@/components/HeaderNav.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CaseView from './components/CaseView.vue'
import CaseList from './components/CaseList.vue'
import CaseForm from './components/CaseForm.vue'

const caseFilter = reactive<PostFilter>({
  board: 2,
  category: null,
  is_com: false,
  project: '',
  ordering: '',
  search: '',
  page: 1,
})

const listFiltering = (payload: PostFilter) => {
  caseFilter.is_com = payload.is_com
  if (!payload.is_com) caseFilter.project = payload.project
  caseFilter.ordering = payload.ordering
  caseFilter.search = payload.search
  fetchPostList({ ...caseFilter })
}

const selectCate = (cate: number) => {
  caseFilter.category = cate
  listFiltering(caseFilter)
}

const pageSelect = (page: number) => {
  caseFilter.page = page
  listFiltering(caseFilter)
}

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
      name: '본사 소송문서 - 보기',
      params: { postId: payload.pk },
    })
  } else {
    createPost(payload)
    router.replace({ name: '본사 소송문서' })
  }
}

const postHit = (payload: PatchPost) => patchPost(payload)
const linkHit = (payload: Link) => patchLink(payload)
const fileHit = (payload: AFile) => patchFile(payload)

onBeforeMount(() => {
  fetchCategoryList(2)
  fetchPostList({ board: 2 })
})

onBeforeUpdate(() => {
  fetchPostList({
    board: 2,
    page: caseFilter.page,
    category: caseFilter.category,
  })
})
</script>

<template>
  <ContentBody>
    <CCardBody class="pb-5">
      <HeaderNav :menus="navMenu" />

      <div v-if="$route.name === '본사 소송사건'" class="pt-3">
        <ListController @list-filter="listFiltering" />

        <CaseList
          :page="caseFilter.page"
          :post-list="postList"
          @page-select="pageSelect"
        />
      </div>

      <div v-else-if="$route.name.includes('보기')">
        <CaseView
          :category="caseFilter.category"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
        />
      </div>

      <div v-else-if="$route.name.includes('작성')">
        <CaseForm :category-list="categoryList" @on-submit="onSubmit" />
      </div>

      <div v-else-if="$route.name.includes('수정')">
        <CaseForm :category-list="categoryList" @on-submit="onSubmit" />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
