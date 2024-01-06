<script lang="ts" setup="">
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useDocument } from '@/store/pinia/document'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import TrashPostList from './components/TrashPostList.vue'
import TrashPostView from './components/TrashPostView.vue'

const mainViewName = ref('휴지통')
const page = ref<number>(1)

const docStore = useDocument()
const trashPost = computed(() => docStore.trashPost)
const trashPostList = computed(() => docStore.trashPostList)
const trashPostCount = computed(() => docStore.trashPostCount)

const fetchTrashPostList = (page?: number) => docStore.fetchTrashPostList(page)
// const patchScrape = (pk: number, title: string) => accStore.patchScrape(pk, title)
// const deleteScrape = (pk: number) => accStore.deleteScrape(pk)

// const patchTitle = (pk: number, title: string) => patchScrape(pk, title)
// const delScrape = (pk: number) => deleteScrape(pk)

const pageSelect = (p: number) => {
  page.value = p
  fetchTrashPostList(p)
}

onBeforeMount(() => fetchTrashPostList(page.value))
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
        <TrashPostView :post="trashPost" />
      </div>
    </CCardBody>
  </ContentBody>
</template>
