<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { type Site } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
import { write_project_site } from '@/utils/pageAuth'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import AddSite from './components/AddSite.vue'
import SiteList from './components/SiteList.vue'

const listControl = ref()

const dataFilter = ref({
  page: 1,
  search: '',
})

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const isReturned = computed(() => projStore.project?.is_returned_area)

const siteStore = useSite()
const getSitesTotal = computed(() => siteStore.getSitesTotal)
const totalArea = computed(() =>
  isReturned.value ? getSitesTotal.value?.returned : getSitesTotal.value?.official,
)

const excelUrl = computed(
  () => `excel/sites/?project=${project.value}&search=${dataFilter.value.search}`,
)

type filter = {
  page: number
  search: string
}

const listFiltering = (payload: filter) => {
  dataFilter.value = payload
  if (project.value) siteStore.fetchSiteList(project.value, payload.page, payload.search)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  if (project.value) siteStore.fetchSiteList(project.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: Site & filter) => siteStore.createSite(payload)

const onUpdate = (payload: Site & filter) => siteStore.updateSite(payload)

const multiSubmit = (payload: Site) => {
  const { page, search } = dataFilter.value
  const submitData = { ...payload, page, search }
  if (payload.pk) onUpdate(submitData)
  else onCreate(submitData)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSite(pk, project)
}

const dataSetup = (pk: number) => siteStore.fetchSiteList(pk)

const dataReset = () => {
  siteStore.siteList = []
  siteStore.siteCount = 0
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => dataSetup(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="ProjectSelect"
    @proj-select="projSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController
        ref="listControl"
        :project="project as number"
        :is-returned="isReturned"
        @list-filtering="listFiltering"
      />
      <AddSite v-if="write_project_site" :project="project as number" @multi-submit="multiSubmit" />
      <TableTitleRow title="사업 부지 목록" excel :url="excelUrl" :disabled="!project">
        <span v-if="project" class="pt-1 text-success">
          총 면적 : {{ numFormat(totalArea as number, 2) }}m<sup>2</sup> ({{
            numFormat((totalArea as number) * 0.3025, 2)
          }}
          평) 등록
        </span>
      </TableTitleRow>
      <SiteList
        :is-returned="isReturned"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>
  </ContentBody>
</template>
