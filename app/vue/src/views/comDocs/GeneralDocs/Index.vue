<script setup lang="ts">
import { ref, computed, onBeforeMount, onBeforeUpdate } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin1'
import { useRouter } from 'vue-router'
import { useCompany } from '@/store/pinia/company'
import { useDocument, PostFilter } from '@/store/pinia/document'
import { AFile, Attatches, Link, Post, PatchPost } from '@/store/types/document'
import { formUtility } from '@/utils/helper'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsList from './components/DocsList.vue'
import DocsView from './components/DocsView.vue'
import DocsForm from './components/DocsForm.vue'

const fController = ref()
const postFilter = ref<PostFilter>({
  company: null,
  board: 2,
  category: null,
  is_com: false,
  project: '',
  ordering: '',
  search: '',
  page: 1,
})

const docsFilter = (payload: PostFilter) => {
  postFilter.value.is_com = payload.is_com
  if (!payload.is_com) postFilter.value.project = payload.project
  postFilter.value.ordering = payload.ordering
  postFilter.value.search = payload.search
  fetchPostList({ ...postFilter.value })
}

const selectCate = (cate: number) => {
  postFilter.value.category = cate
  docsFilter(postFilter.value)
}
const pageSelect = (page: number) => console.log(page)

const comStore = useCompany()
const initComId = computed(() => comStore.initComId)
const company = computed(() => comStore.company?.pk || initComId.value)

const documentStore = useDocument()
const postList = computed(() => documentStore.postList)
const categoryList = computed(() => documentStore.categoryList)

const fetchPostList = (payload: PostFilter) =>
  documentStore.fetchPostList(payload)
const fetchCategoryList = (board: number) =>
  documentStore.fetchCategoryList(board)

const createPost = (payload: { form: FormData }) =>
  documentStore.createPost(payload)
const updatePost = (payload: { pk: number; form: FormData }) =>
  documentStore.updatePost(payload)
const patchPost = (payload: PatchPost) => documentStore.patchPost(payload)
const patchLink = (payload: Link) => documentStore.patchLink(payload)
const patchFile = (payload: AFile) => documentStore.patchFile(payload)

const headerSelect = (target: number) => {
  if (!!target) {
    fetchPostList({ company: target, board: 2 })
  } else {
    documentStore.postList = []
  }
}

const router = useRouter()
const onSubmit = (payload: Post & Attatches) => {
  const { pk, ...formData } = payload
  formData.company = company.value
  const form = formUtility.getFormData(formData)

  console.log(formData)
  console.log(...form)

  if (pk) {
    updatePost({ pk, form })
    router.replace({
      name: '본사 일반 문서 - 보기',
      params: { postId: pk },
    })
  } else {
    createPost({ form })
    router.replace({ name: '본사 일반 문서' })
  }
}

const postHit = (payload: PatchPost) => patchPost(payload)
const linkHit = (payload: Link) => patchLink(payload)
const fileHit = (payload: AFile) => patchFile(payload)

const sortFilter = (project: number | null) => {
  fController.value.projectChange(project)
  postFilter.value.page = 1
  if (project !== null) postFilter.value.project = project.toString()
  else postFilter.value.is_com = true
  docsFilter(postFilter.value)
}

onBeforeMount(() => {
  fetchCategoryList(2)
  fetchPostList({ company: company.value, board: 2 })
})

onBeforeUpdate(() => {
  fetchPostList({
    company: company.value,
    board: 2,
    page: postFilter.value.page,
    category: postFilter.value.category,
  })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="headerSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="$route.name === '본사 일반 문서'" class="pt-3">
        <ListController ref="fController" @docs-filter="docsFilter" />

        <CategoryTabs
          :category="postFilter.category"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :page="postFilter.page"
          :post-list="postList"
          @page-select="pageSelect"
          @sort-filter="sortFilter"
        />
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
