<script lang="ts" setup="">
import { computed, onBeforeMount, ref } from 'vue'
import { navMenu, pageTitle } from '@/views/_MyPage/_menu/headermixin'
import { useAccount } from '@/store/pinia/account'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ScrapeList from '@/views/_MyPage/OwnScrap/components/ScrapeList.vue'

const mainViewName = ref('스크랩')

const accStore = useAccount()
const scrapeList = computed(() => accStore.scrapeList)

const fetchScrapeList = () => accStore.fetchScrapeList()

onBeforeMount(() => fetchScrapeList())
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <div class="pt-3">
        <ScrapeList :scrpae-list="scrapeList" :view-route="mainViewName" />
      </div>
    </CCardBody>
  </ContentBody>
</template>
