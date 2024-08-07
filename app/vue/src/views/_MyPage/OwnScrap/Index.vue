<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useAccount } from '@/store/pinia/account'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ScrapeList from '@/views/_MyPage/OwnScrap/components/ScrapeList.vue'

const mainViewName = ref('스크랩')
const sort = ref<'docs' | 'board'>('docs')
const page = ref<number>(1)

const accStore = useAccount()
const docScrapeList = computed(() => accStore.docScrapeList)
const scrapeList = computed(() => accStore.scrapeList)
const scrapeCount = computed(() => accStore.scrapeCount)

const fetchScrapeList = (page?: number) => accStore.fetchScrapeList(page)
const patchScrape = (pk: number, title: string) => accStore.patchScrape(pk, title)
const deleteScrape = (pk: number) => accStore.deleteScrape(pk)

const patchTitle = (pk: number, title: string) => patchScrape(pk, title)
const delScrape = (pk: number) => deleteScrape(pk)

const pageSelect = (p: number) => {
  page.value = p
  fetchScrapeList(p)
}

onBeforeMount(() => fetchScrapeList(page.value))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div class="pt-3">
        <CRow class="pb-2">
          <CCol sm="12" lg="9" xl="6">
            <CRow>
              <CCol class="d-grid gap-2 pr-0">
                <CFormCheck
                  v-model="sort"
                  value="docs"
                  :button="{
                    color: 'primary',
                    variant: 'outline',
                    shape: 'rounded-0',
                  }"
                  type="radio"
                  name="options-outlined"
                  id="primary-outlined"
                  label="문서"
                />
              </CCol>
              <CCol class="d-grid gap-2 pl-0">
                <CFormCheck
                  v-model="sort"
                  value="board"
                  :button="{ color: 'success', variant: 'outline', shape: 'rounded-0' }"
                  type="radio"
                  name="options-outlined"
                  id="success-outlined"
                  label="게시글"
                />
              </CCol>
            </CRow>
          </CCol>
        </CRow>

        <ScrapeList
          v-if="sort === 'docs'"
          :doc-scrape-list="docScrapeList"
          :scrape-list="scrapeList"
          :scrape-count="scrapeCount"
          :view-route="mainViewName"
          :page="page"
          @patch-title="patchTitle"
          @del-scrape="delScrape"
          @page-select="pageSelect"
        />
        <div v-else>???</div>
      </div>
    </CCardBody>
  </ContentBody>
</template>
