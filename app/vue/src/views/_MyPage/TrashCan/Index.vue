<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useDocs } from '@/store/pinia/docs'
import type { TrashDocs as TP } from '@/store/types/docs'
import { type RouteLocationNormalizedLoaded as LoadedRoute, useRoute, useRouter } from 'vue-router'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import TrashDocsList from './components/TrashDocsList.vue'
import TrashDocsView from './components/TrashDocsView.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

const mainViewName = ref('휴지통')
const category = ref()
const page = ref<number>(1)

const docStore = useDocs()
const trashDocs = computed(() => docStore.trashDocs)
const trashDocsList = computed(() => docStore.trashDocsList)
const trashDocsCount = computed(() => docStore.trashDocsCount)

const fetchTrashDocs = (pk: number) => docStore.fetchTrashDocs(pk)
const fetchTrashDocsList = (page?: number) => docStore.fetchTrashDocsList(page)
const restoreDocs = (pk: number) => docStore.restoreDocs(pk)

const [route, router] = [
  useRoute() as LoadedRoute & {
    name: string
  },
  useRouter(),
]

watch(route, val => {
  if (val.params.docsId) fetchTrashDocs(Number(val.params.docsId))
  else docStore.trashDocs = null
})

const pageSelect = (p: number) => {
  page.value = p
  fetchTrashDocsList(p)
}

const restoreId = ref<number | null>(null)

const refRestoreModal = ref()
const callRestoreDocs = (pk: number) => {
  restoreId.value = pk
  refRestoreModal.value.callModal()
}

const modalAction = () => {
  restoreDocs(restoreId.value as number)
  refRestoreModal.value.close()
  router.replace({ name: mainViewName.value })
}

const docsId = computed(() => Number(route.params.docsId))

onBeforeMount(() => {
  fetchTrashDocsList(page.value)
  if (docsId.value) fetchTrashDocs(docsId.value)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div v-if="route.name === mainViewName" class="pt-3">
        <TrashDocsList
          :trash-docs-list="trashDocsList"
          :trash-docs-count="trashDocsCount"
          :view-route="mainViewName"
          :page="page"
          @page-select="pageSelect"
          @restore-docs="callRestoreDocs"
        />
      </div>

      <div v-else-if="route.name.includes('보기')" class="pt-3">
        <TrashDocsView
          :category="category as undefined"
          :docs="trashDocs as TP"
          :view-route="mainViewName"
          :curr-page="page"
          @restore-docs="callRestoreDocs"
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
