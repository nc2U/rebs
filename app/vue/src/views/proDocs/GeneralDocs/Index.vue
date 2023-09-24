<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/proDocs/_menu/headermixin1'
import { type RouteLocationNormalizedLoaded as Loaded, useRoute, useRouter } from 'vue-router'
import { useProject } from '@/store/pinia/project'
import { useDocument, type PostFilter } from '@/store/pinia/document'
import {
  type AFile,
  type Attatches,
  type Link,
  type Post,
  type PatchPost,
} from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListingProDocs from '@/components/Documents/ListingProDocs.vue'
import CategoryTabs from '@/components/Documents/CategoryTabs.vue'
import DocsList from '@/components/Documents/DocsList.vue'
import DocsView from '@/components/Documents/DocsView.vue'
import DocsForm from '@/components/Documents/DocsForm.vue'

const fController = ref()
const boardNumber = ref(2)
const mainViewName = ref('현장 일반 문서')
const postFilter = ref<PostFilter>({
  company: '',
  board: boardNumber.value,
  category: '',
  is_com: false,
  project: '',
  ordering: '',
  search: '',
  page: 1,
})

const newFiles = ref<File[]>([])
const cngFiles = ref<
  {
    pk: number
    file: File
  }[]
>([])

const docsFilter = (payload: PostFilter) => {
  postFilter.value.ordering = payload.ordering
  postFilter.value.search = payload.search
  if (project.value) fetchPostList({ ...postFilter.value })
}

const selectCate = (cate: number) => {
  postFilter.value.category = cate
  docsFilter(postFilter.value)
}

const pageSelect = (page: number) => {
  postFilter.value.page = page
  docsFilter(postFilter.value)
}

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const company = computed(() => projStore.project?.company)

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)
const categoryList = computed(() => docStore.categoryList)

const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)
const fetchCategoryList = (board: number) => docStore.fetchCategoryList(board)

const createPost = (payload: { form: FormData }) => docStore.createPost(payload)
const updatePost = (payload: { pk: number; form: FormData }) => docStore.updatePost(payload)
const patchPost = (payload: PatchPost) => docStore.patchPost(payload)
const patchLink = (payload: Link) => docStore.patchLink(payload)
const patchFile = (payload: AFile) => docStore.patchFile(payload)

const [route, router] = [
  useRoute() as Loaded & {
    name: string
  },
  useRouter(),
]

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else docStore.post = null
})

const fileChange = (payload: { pk: number; file: File }) => cngFiles.value.push(payload)

const fileUpload = (file: File) => newFiles.value.push(file)

const onSubmit = (payload: Post & Attatches) => {
  if (project.value) {
    const { pk, ...getData } = payload
    getData.company = company.value as null | number
    getData.project = project.value
    getData.newFiles = newFiles.value
    getData.cngFiles = cngFiles.value

    const form = new FormData()

    for (const key in getData) {
      if (key === 'links' || key === 'files') {
        getData[key]?.forEach(val => form.append(key, JSON.stringify(val)))
      } else if (key === 'newLinks' || key === 'newFiles' || key === 'cngFiles') {
        if (key === 'cngFiles') {
          getData[key]?.forEach(val => {
            form.append('cngPks', val.pk as any)
            form.append('cngFiles', val.file as Blob)
          })
        } else getData[key]?.forEach(val => form.append(key, val as string | Blob))
      } else {
        const formValue = getData[key] === null ? '' : getData[key]
        form.append(key, formValue as string)
      }
    }

    if (pk) {
      updatePost({ pk, form })
      router.replace({
        name: `${mainViewName.value} - 보기`,
        params: { postId: pk },
      })
    } else {
      createPost({ form })
      router.replace({ name: `${mainViewName.value}` })
    }
  }
}

const postHit = (payload: PatchPost) => patchPost(payload)
const linkHit = (payload: Link) => patchLink(payload)
const fileHit = (payload: AFile) => patchFile(payload)

const sortFilter = (project: number | null) => {
  fController.value.projectChange(project)
  postFilter.value.page = 1
  if (project !== null) postFilter.value.project = project
  else postFilter.value.is_com = true
  docsFilter(postFilter.value)
}

const dataSetup = (pk: number, postId?: string | string[]) => {
  fetchPostList({
    project: pk,
    board: boardNumber.value,
    page: postFilter.value.page,
    category: postFilter.value.category,
  })
  if (postId) fetchPost(Number(postId))
  postFilter.value.project = pk
}

const dataReset = () => {
  docStore.post = null
  docStore.postList = []
  docStore.postCount = 0
  postFilter.value.company = ''
  router.replace({ name: `${mainViewName.value}` })
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  fetchCategoryList(boardNumber.value)
  dataSetup(project.value || projStore.initProjId, route.params?.postId)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === `${mainViewName}`" class="pt-3">
        <ListingProDocs ref="fController" @docs-filter="docsFilter" />

        <CategoryTabs
          :category="postFilter.category as number"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :project="project as number"
          :page="postFilter.page"
          :post-list="postList"
          :view-route="mainViewName"
          @page-select="pageSelect"
          @sort-filter="sortFilter"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <DocsView
          :category="postFilter.category as number"
          :post="post as Post"
          :view-route="mainViewName"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
        />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <DocsForm
          :board-num="boardNumber"
          :category-list="categoryList"
          :view-route="mainViewName"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <DocsForm
          :board-num="boardNumber"
          :category-list="categoryList"
          :post="post as Post"
          :view-route="mainViewName"
          @file-change="fileChange"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
