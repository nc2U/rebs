<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin2'
import { formUtility } from '@/utils/helper'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import { useCompany } from '@/store/pinia/company'
import { type PostFilter, type SuitCaseFilter, useDocument } from '@/store/pinia/document'
import {
  type AFile,
  type Attatches,
  type Link,
  type PatchPost,
  type Post,
} from '@/store/types/document'
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

const newFiles = ref<File[]>([])

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
const company = computed(() => comStore.company?.pk)

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)
const categoryList = computed(() => docStore.categoryList)
const getSuitCase = computed(() => docStore.getSuitCase)

const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)
const fetchCategoryList = (board: number) => docStore.fetchCategoryList(board)
const fetchAllSuitCaseList = (payload: SuitCaseFilter) => docStore.fetchAllSuitCaseList(payload)

const createPost = (payload: { formData: FormData }) => docStore.createPost(payload)
const updatePost = (payload: { pk: number; formData: FormData }) => docStore.updatePost(payload)
const patchPost = (payload: PatchPost) => docStore.patchPost(payload)
const patchLink = (payload: Link) => docStore.patchLink(payload)
const patchFile = (payload: AFile) => docStore.patchFile(payload)

const [route, router] = [useRoute() as LoadedRoute & { name: string }, useRouter()]

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else docStore.post = null
})

const fileUpload = (file: File) => newFiles.value.push(file)

const onSubmit = (payload: Post & Attatches) => {
  // if (payload.files?.length) for (const file of payload.files) console.log(file)

  if (company.value) {
    const { pk, ...form } = payload
    form.company = company.value
    form.newFiles = newFiles.value
    console.log(form)

    const formData = new FormData()

    for (const key in form) formData.append(key, form[key] as string | Blob)

    console.log(formData)

    // if (pk) {
    //   updatePost({ pk, formData })
    //   router.replace({
    //     name: '본사 소송 문서 - 보기',
    //     params: { postId: pk },
    //   })
    // } else {
    //   createPost({ formData })
    //   router.replace({ name: '본사 소송 문서' })
    // }
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

const dataSetup = (pk: number, postId?: string | string[]) => {
  fetchPostList({
    company: pk,
    board: 3,
    page: caseFilter.value.page,
    category: caseFilter.value.category,
  })
  fetchAllSuitCaseList({})
  if (postId) fetchPost(Number(postId))
  caseFilter.value.company = pk
}
const dataReset = () => {
  comStore.company = null
  docStore.post = null
  docStore.postList = []
  docStore.postCount = 0
  caseFilter.value.company = null
  router.replace({ name: '본사 소송 문서' })
}

const comSelect = (target: number | null) => {
  dataReset()
  if (target) dataSetup(target)
}

onBeforeMount(() => {
  fetchCategoryList(3)
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
      <div v-if="route.name === '본사 소송 문서'" class="pt-3">
        <ListController ref="fController" @list-filter="listFiltering" />

        <CategoryTabs
          :category="caseFilter.category || undefined"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :company="company || undefined"
          :page="caseFilter.page"
          :post-list="postList"
          @page-select="pageSelect"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <DocsView
          :category="caseFilter.category as undefined"
          :post="post as Post"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
        />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <DocsForm
          :category-list="categoryList"
          :get-suit-case="getSuitCase"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <DocsForm
          :category-list="categoryList"
          :get-suit-case="getSuitCase"
          :post="post as Post"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
