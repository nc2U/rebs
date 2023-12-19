<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/comDocs/_menu/headermixin2'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import { useAccount } from '@/store/pinia/account'
import { useCompany } from '@/store/pinia/company'
import { type PostFilter, type SuitCaseFilter, useDocument } from '@/store/pinia/document'
import type { AFile, Attatches, Link, PatchPost, Post } from '@/store/types/document'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/components/Documents/ListController.vue'
import CategoryTabs from '@/components/Documents/CategoryTabs.vue'
import DocsList from '@/components/Documents/DocsList.vue'
import DocsView from '@/components/Documents/DocsView.vue'
import DocsForm from '@/components/Documents/DocsForm.vue'

const fController = ref()
const boardNumber = ref(3)
const mainViewName = ref('본사 소송 문서')
const postFilter = ref<PostFilter>({
  company: '',
  project: '',
  board: boardNumber.value,
  is_com: true,
  category: '',
  lawsuit: '',
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
  postFilter.value.project = !!payload.is_com ? '' : payload.project
  postFilter.value.is_com = payload.is_com
  postFilter.value.lawsuit = payload.lawsuit
  postFilter.value.ordering = payload.ordering
  postFilter.value.search = payload.search
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

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)

const accStore = useAccount()
const likePosts = computed(() => accStore.likePosts)
const writeAuth = computed(() => accStore.writeComDocs)

const docStore = useDocument()
const post = computed(() => docStore.post)
const postList = computed(() => docStore.postList)
const categoryList = computed(() => docStore.categoryList)
const getSuitCase = computed(() => docStore.getSuitCase)

const fetchLink = (pk: number) => docStore.fetchLink(pk)
const fetchFile = (pk: number) => docStore.fetchFile(pk)
const fetchPost = (pk: number) => docStore.fetchPost(pk)
const fetchPostList = (payload: PostFilter) => docStore.fetchPostList(payload)
const fetchCategoryList = (board: number) => docStore.fetchCategoryList(board)
const fetchAllSuitCaseList = (payload: SuitCaseFilter) => docStore.fetchAllSuitCaseList(payload)

const createPost = (payload: { form: FormData }) => docStore.createPost(payload)
const updatePost = (payload: { pk: number; form: FormData }) => docStore.updatePost(payload)
const patchPost = (payload: PatchPost & { filter: PostFilter }) => docStore.patchPost(payload)
const patchLink = (payload: Link) => docStore.patchLink(payload)
const patchFile = (payload: AFile) => docStore.patchFile(payload)
const patchPostLike = (pk: number) => docStore.patchPostLike(pk)

const [route, router] = [
  useRoute() as LoadedRoute & {
    name: string
  },
  useRouter(),
]

watch(route, val => {
  if (val.params.postId) fetchPost(Number(val.params.postId))
  else docStore.post = null
})

const toLike = (pk: number) => patchPostLike(pk)

const postsRenewal = (page: number) => {
  postFilter.value.page = page
  fetchPostList(postFilter.value)
}
const fileChange = (payload: { pk: number; file: File }) => cngFiles.value.push(payload)

const fileUpload = (file: File) => newFiles.value.push(file)

const onSubmit = async (payload: Post & Attatches) => {
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
      fController.value.resetForm()
    }
    newFiles.value = []
    cngFiles.value = []
  }
}

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

const dataSetup = (pk: number, postId?: string | string[]) => {
  postFilter.value.company = pk
  fetchCategoryList(boardNumber.value)
  fetchAllSuitCaseList({ is_com: true })
  fetchPostList(postFilter.value)
  if (postId) fetchPost(Number(postId))
}
const dataReset = () => {
  comStore.company = null
  docStore.post = null
  docStore.postList = []
  docStore.postCount = 0
  postFilter.value.company = ''
  router.replace({ name: `${mainViewName.value}` })
}

const comSelect = (target: number | null) => {
  dataReset()
  if (target) dataSetup(target)
}

onBeforeMount(() => dataSetup(company.value || comStore.initComId, route.params?.postId))
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
      <div v-if="route.name === `${mainViewName}`" class="pt-3">
        <ListController
          ref="fController"
          :com-from="true"
          :get-suit-case="getSuitCase"
          :post-filter="postFilter"
          @list-filter="listFiltering"
        />

        <CategoryTabs
          :category="postFilter.category || undefined"
          :category-list="categoryList"
          @select-cate="selectCate"
        />

        <DocsList
          :company="company || undefined"
          :page="postFilter.page ?? 1"
          :post-list="postList"
          :view-route="mainViewName"
          :is-lawsuit="true"
          :write-auth="writeAuth"
          @page-select="pageSelect"
        />
      </div>

      <div v-else-if="route.name.includes('보기')">
        <DocsView
          :board-num="boardNumber"
          :heated-page="heatedPage"
          :re-order="postFilter.ordering !== '-created'"
          :category="postFilter.category as undefined"
          :post="post as Post"
          :like-posts="likePosts"
          :view-route="mainViewName"
          :curr-page="postFilter.page ?? 1"
          :write-auth="writeAuth"
          @to-like="toLike"
          @post-hit="postHit"
          @link-hit="linkHit"
          @file-hit="fileHit"
          @posts-renewal="postsRenewal"
        />
      </div>

      <div v-else-if="route.name.includes('작성')">
        <DocsForm
          :board-num="boardNumber"
          :category-list="categoryList"
          :get-suit-case="getSuitCase"
          :view-route="mainViewName"
          :write-auth="writeAuth"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>

      <div v-else-if="route.name.includes('수정')">
        <DocsForm
          :board-num="boardNumber"
          :category-list="categoryList"
          :get-suit-case="getSuitCase"
          :post="post as Post"
          :view-route="mainViewName"
          :write-auth="writeAuth"
          @file-change="fileChange"
          @file-upload="fileUpload"
          @on-submit="onSubmit"
        />
      </div>
    </CCardBody>
  </ContentBody>
</template>
