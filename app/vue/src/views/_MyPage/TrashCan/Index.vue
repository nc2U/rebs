<script lang="ts" setup="">
import { computed, onBeforeMount, ref, watch } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useDocument } from '@/store/pinia/document'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute } from 'vue-router'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import TrashPostList from './components/TrashPostList.vue'
import TrashPostView from './components/TrashPostView.vue'

const mainViewName = ref('휴지통')
const category = ref()
const page = ref<number>(1)

const docStore = useDocument()
const trashPost = computed(() => docStore.trashPost)
const trashPostList = computed(() => docStore.trashPostList)
const trashPostCount = computed(() => docStore.trashPostCount)

const fetchTrashPost = (pk: number) => docStore.fetchTrashPost(pk)
const fetchTrashPostList = (page?: number) => docStore.fetchTrashPostList(page)

const route = useRoute() as LoadedRoute & {
  name: string
}

watch(route, val => {
  if (val.params.postId) fetchTrashPost(Number(val.params.postId))
  else docStore.trashPost = null
})

const pageSelect = (p: number) => {
  page.value = p
  fetchTrashPostList(p)
}

const restorePost = () => alert('ok!')

const postId = computed(() => Number(route.params.postId))

onBeforeMount(() => {
  fetchTrashPostList(page.value)
  if (postId.value) fetchTrashPost(postId.value)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="$route.name === mainViewName" class="pt-3">
        <TrashPostList
          :trash-post-list="trashPostList"
          :trash-post-count="trashPostCount"
          :view-route="mainViewName"
          :page="page"
          @page-select="pageSelect"
        />
      </div>

      <div v-else-if="$route.name.includes('보기')" class="pt-3">
        <TrashPostView
          :category="category as undefined"
          :post="trashPost"
          :view-route="mainViewName"
          :curr-page="page"
          @restore-post="restorePost"
        />
      </div>
    </CCardBody>
  </ContentBody>
</template>
