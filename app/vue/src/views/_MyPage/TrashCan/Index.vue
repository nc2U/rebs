<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useDocument } from '@/store/pinia/document'
import type { TrashPost as TP } from '@/store/types/document'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import TrashPostList from './components/TrashPostList.vue'
import TrashPostView from './components/TrashPostView.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const mainViewName = ref('휴지통')
const category = ref()
const page = ref<number>(1)

const docStore = useDocument()
const trashPost = computed(() => docStore.trashPost)
const trashPostList = computed(() => docStore.trashPostList)
const trashPostCount = computed(() => docStore.trashPostCount)

const fetchTrashPost = (pk: number) => docStore.fetchTrashPost(pk)
const fetchTrashPostList = (page?: number) => docStore.fetchTrashPostList(page)
const restorePost = (pk: number) => docStore.restorePost(pk)

const [route, router] = [
  useRoute() as LoadedRoute & {
    name: string
  },
  useRouter(),
]

watch(route, val => {
  if (val.params.postId) fetchTrashPost(Number(val.params.postId))
  else docStore.trashPost = null
})

const pageSelect = (p: number) => {
  page.value = p
  fetchTrashPostList(p)
}

const restoreId = ref<number | null>(null)

const refRestoreModal = ref()
const callRestorePost = (pk: number) => {
  restoreId.value = pk
  refRestoreModal.value.callModal()
}

const modalAction = () => {
  restorePost(restoreId.value as number)
  refRestoreModal.value.close()
  router.replace({ name: mainViewName.value })
}

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
      <div v-if="route.name === mainViewName" class="pt-3">
        <TrashPostList
          :trash-post-list="trashPostList"
          :trash-post-count="trashPostCount"
          :view-route="mainViewName"
          :page="page"
          @page-select="pageSelect"
          @restore-post="callRestorePost"
        />
      </div>

      <div v-else-if="route.name.includes('보기')" class="pt-3">
        <TrashPostView
          :category="category as undefined"
          :post="trashPost as TP"
          :view-route="mainViewName"
          :curr-page="page"
          @restore-post="callRestorePost"
        />
      </div>
    </CCardBody>
  </ContentBody>

  <ConfirmModal ref="refRestoreModal">
    <template #header>알림</template>
    <template #default>이 게시물을 휴지통으로부터 복원 하시겠습니까?</template>
    <template #footer>
      <CButton color="success" @click="modalAction">삭제 복원</CButton>
    </template>
  </ConfirmModal>
</template>
