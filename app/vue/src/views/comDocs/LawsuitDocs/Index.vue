<script setup lang="ts">
import { ref, computed, onBeforeMount, onBeforeUpdate } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin2'
import { formUtility } from '@/utils/helper'
import { useRouter } from 'vue-router'
import { useCompany } from '@/store/pinia/company'
import { PostFilter, useDocument } from '@/store/pinia/document'
import { AFile, Attatches, Link, PatchPost, Post } from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import DocsView from './components/DocsView.vue'
import DocsList from './components/DocsList.vue'
import DocsForm from './components/DocsForm.vue'

const fController = ref()
const caseFilter = ref<PostFilter>({
  company: null,
  board: 3,
  category: null,
  is_com: '',
  project: '',
  ordering: '',
  search: '',
  page: 1,
})

const listFiltering = (payload: PostFilter) => {
  caseFilter.value.is_com = payload.is_com
  if (!payload.is_com) caseFilter.value.project = payload.project
  caseFilter.value.ordering = payload.ordering
  caseFilter.value.search = payload.search
  if (company.value) fetchPostList({ ...caseFilter.value })
}

const selectCate = (cate: number) => {
  caseFilter.value.category = cate
  listFiltering(caseFilter.value)
}

const pageSelect = (page: number) => {
  caseFilter.value.page = page
  listFiltering(caseFilter.value)
}

const comStore = useCompany()
const initComId = computed(() => comStore.initComId)
const company = computed(() => comStore.company?.pk || null)

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

const router = useRouter()

const companySelect = (target: number) => {
  if (!!target) {
    fetchPostList({ company: target, board: 3 })
  } else {
    comStore.company = null
    documentStore.postList = []
    documentStore.postCount = 0
    router.replace({ name: '본사 소송 문서' })
  }
}

const onSubmit = (payload: Post & Attatches) => {
  const { pk, ...formData } = payload
  formData.company = company.value
  const form = formUtility.getFormData(formData)

  console.log(formData, ...form)

  if (pk) {
    updatePost({ pk, form })
    router.replace({
      name: '본사 소송 문서 - 보기',
      params: { postId: pk },
    })
  } else {
    createPost({ form })
    router.replace({ name: '본사 소송 문서' })
  }
}

const postHit = (payload: PatchPost) => patchPost(payload)
const linkHit = (payload: Link) => patchLink(payload)
const fileHit = (payload: AFile) => patchFile(payload)

const sortFilter = (project: number | null) => {
  fController.value.projectChange(project)
  caseFilter.value.page = 1
  if (project !== null) caseFilter.value.project = project.toString()
  else caseFilter.value.is_com = true
  listFiltering(caseFilter.value)
}

onBeforeMount(() => {
  fetchCategoryList(3)
  caseFilter.value.company = company.value || initComId.value
  fetchPostList({ company: company.value || initComId.value, board: 3 })
})

onBeforeUpdate(() => {
  if (company.value)
    fetchPostList({
      company: company.value,
      board: 3,
      page: caseFilter.value.page,
      category: caseFilter.value.category,
    })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="companySelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="$route.name === '본사 소송 문서'" class="pt-3">
        <ListController ref="fController" @list-filter="listFiltering" />

        <CategoryTabs
          :category="caseFilter.category"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :company="company"
          :page="caseFilter.page"
          :post-list="postList"
          @page-select="pageSelect"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="$route.name.includes('보기')">
        <DocsView
          :category="caseFilter.category"
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
