<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin1'
import { useRoute, useRouter } from 'vue-router'
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
  if (company.value) fetchPostList({ ...postFilter.value })
}

const selectCate = (cate: number) => {
  postFilter.value.category = cate
  docsFilter(postFilter.value)
}

const pageSelect = (page: number) => {
  postFilter.value.page = page
  docsFilter(postFilter.value)
}

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)
const categoryList = computed(() => docStore.categoryList)

const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)
const fetchCategoryList = (board: number) => docStore.fetchCategoryList(board)

const createPost = (payload: { form: FormData }) => docStore.createPost(payload)
const updatePost = (payload: { pk: number; form: FormData }) =>
  docStore.updatePost(payload)
const patchPost = (payload: PatchPost) => docStore.patchPost(payload)
const patchLink = (payload: Link) => docStore.patchLink(payload)
const patchFile = (payload: AFile) => docStore.patchFile(payload)

const [route, router] = [useRoute(), useRouter()]

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else docStore.post = null
})

const onSubmit = (payload: Post & Attatches) => {
  const { pk, ...formData } = payload
  formData.company = company.value || null
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

const dataSetup = (pk: number, postId?: string | string[]) => {
  fetchPostList({
    company: pk,
    board: 2,
    page: postFilter.value.page,
    category: postFilter.value.category,
  })
  postFilter.value.company = pk
  if (postId) fetchPost(Number(postId))
}

const dataReset = () => {
  comStore.company = null
  docStore.post = null
  docStore.postList = []
  docStore.postCount = 0
  postFilter.value.company = null
  router.replace({ name: '본사 일반 문서' })
}

const comSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  fetchCategoryList(2)
  dataSetup(company.value || comStore.initComId, route.params?.postId)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @com-select="comSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === '본사 일반 문서'" class="pt-3">
        <ListController ref="fController" @docs-filter="docsFilter" />

        <CategoryTabs
          :category="postFilter.category"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :company="company"
          :page="postFilter.page"
          :post-list="postList"
          @page-select="pageSelect"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <DocsView
          :category="postFilter.category"
          :post="post"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
        />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <DocsForm :category-list="categoryList" @on-submit="onSubmit" />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <DocsForm
          :category-list="categoryList"
          :post="post"
          @on-submit="onSubmit"
        />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
