<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { Site } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
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

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const isReturned = computed(() => projectStore.project?.is_returned_area)

const siteStore = useSite()
const getSitesTotal = computed(() => siteStore.getSitesTotal)
const totalArea = computed(() =>
  isReturned.value
    ? getSitesTotal.value?.returned
    : getSitesTotal.value?.official,
)

const onSelectAdd = (target: number) => {
  if (!!target) {
    siteStore.fetchSiteList(target)
  } else {
    siteStore.siteList = []
    siteStore.siteCount = 0
  }
}

type filter = {
  page: number
  search: string
}

const listFiltering = (payload: filter) => {
  dataFilter.value = payload
  siteStore.fetchSiteList(project.value, payload.page, payload.search)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  siteStore.fetchSiteList(project.value, page)
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

const excelUrl = 'excel/sites/?project=' + project.value

onBeforeMount(() => siteStore.fetchSiteList(project.value))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController
        ref="listControl"
        :project="project"
        :is-returned="isReturned"
        @list-filtering="listFiltering"
      />
      <AddSite :project="project" @multi-submit="multiSubmit" />
      <TableTitleRow title="사업 부지 목록" excel :url="excelUrl">
        <span class="pt-1 text-success">
          총 면적 : {{ numFormat(totalArea, 2) }}m<sup>2</sup> ({{
            numFormat(totalArea * 0.3025, 2)
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

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
