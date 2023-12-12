<script lang="ts" setup>
import { ref, computed, inject, watch, onBeforeMount } from 'vue'
import { type RouteLocationNormalizedLoaded as Loaded, useRoute, useRouter } from 'vue-router'
import ListController from './components/ListController.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import type { AFile, Attatches, Link, PatchPost, Post } from '@/store/types/document'
import { type PostFilter, useDocument } from '@/store/pinia/document'
import NoticeList from './components/NoticeList.vue'
import NoticeView from './components/NoticeView.vue'
import NoticeForm from '@/views/_Dashboard/components/NoticeBoard/components/NoticeForm.vue'

const lController = ref()
const boardNumber = ref(1)
const mainViewName = ref('공지 사항')

const postFilter = ref<PostFilter>({
  company: '',
  board: boardNumber.value,
  category: '',
  ordering: '-created',
  search: '',
  page: 1,
})

const heatedPage = ref<number[]>([])
const newFiles = ref<File[]>([])
const cngFiles = ref<
  {
    pk: number
    file: File
  }[]
>([])

const listFiltering = (payload: PostFilter) => {
  postFilter.value.ordering = payload.ordering ?? '-created'
  postFilter.value.search = payload.search ?? ''
  if (company.value) fetchPostList({ ...postFilter.value })
}

const selectCate = (cate: number) => {
  postFilter.value.page = 1
  postFilter.value.category = cate
  listFiltering(postFilter.value)
}

const pageSelect = (page: number) => {
  postFilter.value.page = page
  listFiltering(postFilter.value)
}

const comStore = inject('comStore') as any
const company = computed(() => comStore.company?.pk)

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)
const noticeList = computed(() => docStore.noticeList)
const categoryList = computed(() => docStore.categoryList)

const fetchLink = (pk: number) => docStore.fetchLink(pk)
const fetchFile = (pk: number) => docStore.fetchFile(pk)
const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)
const fetchCategoryList = (board: number) => docStore.fetchCategoryList(board)

const createPost = (payload: { form: FormData }) => docStore.createPost(payload)
const updatePost = (payload: { pk: number; form: FormData }) => docStore.updatePost(payload)
const patchPost = (payload: PatchPost & { filter: PostFilter }) => docStore.patchPost(payload)
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

const postsRenewal = (page: number) => {
  postFilter.value.page = page
  fetchPostList(postFilter.value)
}

const fileChange = (payload: { pk: number; file: File }) => cngFiles.value.push(payload)

const fileUpload = (file: File) => newFiles.value.push(file)

const postHit = async (pk: number) => {
  if (!heatedPage.value.includes(pk)) {
    heatedPage.value.push(pk)
    await fetchPost(pk)
    const hit = (post.value?.hit ?? 0) + 1
    await patchPost({ pk, hit, filter: postFilter.value })
  }
}
const linkHit = async (pk: number) => {
  const link = (await fetchLink(pk)) as Link
  link.hit = (link.hit as number) + 1
  await patchLink(link)
}
const fileHit = async (pk: number) => {
  const file = (await fetchFile(pk)) as AFile
  const hit = (file.hit as number) + 1
  await patchFile({ pk, hit })
}

const onSubmit = async (payload: Post & Attatches) => {
  console.log(payload)

  if (company.value) {
    const { pk, ...getData } = payload
    getData.company = company.value
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
      await updatePost({ pk, form })
      await router.replace({
        name: `${mainViewName.value} - 보기`,
        params: { postId: pk },
      })
    } else {
      await createPost({ form })
      await router.replace({ name: `${mainViewName.value}` })
      lController.value.resetForm()
    }
    newFiles.value = []
    cngFiles.value = []
  }
}

const dataSetup = (pk: number, postId?: string | string[]) => {
  postFilter.value.company = pk
  fetchCategoryList(boardNumber.value)
  fetchPostList(postFilter.value)
  if (postId) fetchPost(Number(postId))
}

onBeforeMount(() => dataSetup(company.value ?? comStore.initComId, route.params?.postId))
</script>

<template>
  <CContainer fluid>
    <CCard>
      <CCardBody>
        <h5>{{ mainViewName }}</h5>
        <hr />
        <div v-if="route.name === mainViewName">
          <ListController
            ref="lController"
            :com-from="true"
            :post-filter="postFilter"
            @list-filter="listFiltering"
          />
          <CategoryTabs
            :category="postFilter.category as number"
            :category-list="categoryList"
            @select-cate="selectCate"
          />
          <NoticeList
            :company="company as number"
            :page="postFilter.page"
            :notice-list="noticeList"
            :post-list="postList"
            :view-route="mainViewName"
            @page-select="pageSelect"
          />
        </div>

        <div v-else-if="route.name.includes('보기')">
          <NoticeView
            :board-num="boardNumber"
            :heated-page="heatedPage"
            :re-order="postFilter.ordering !== '-created'"
            :category="postFilter.category as number"
            :post="post as Post"
            :view-route="mainViewName"
            :curr-page="postFilter.page ?? 1"
            @post-hit="postHit"
            @link-hit="linkHit"
            @file-hit="fileHit"
            @posts-renewal="postsRenewal"
          />
        </div>

        <div v-else-if="route.name.includes('작성')">
          <NoticeForm
            :board-num="boardNumber"
            :category-list="categoryList"
            :view-route="mainViewName"
            @file-upload="fileUpload"
            @on-submit="onSubmit"
          />
        </div>

        <div v-else-if="route.name.includes('수정')">
          <NoticeForm
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
    </CCard>
  </CContainer>
</template>
