<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import { numFormat } from '@/utils/baseMixins'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { write_project_site } from '@/utils/pageAuth'
import { type Relation, type SiteOwner } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/projects/SiteOwner/components/ListController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import AddSiteOwner from '@/views/projects/SiteOwner/components/AddSiteOwner.vue'
import SiteOwnerList from '@/views/projects/SiteOwner/components/SiteOwnerList.vue'

const listControl = ref()

type filter = {
  page: number
  own_sort: string
  search: string
}

const dataFilter = ref<filter>({
  page: 1,
  own_sort: '',
  search: '',
})

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const isReturned = computed(() => projStore.project?.is_returned_area)

const siteStore = useSite()
const getOwnersTotal = computed(() => siteStore.getOwnersTotal?.owned_area)

const excelUrl = computed(() => {
  const url = `excel/sites-by-owner/?project=${project.value}`
  const filter = dataFilter.value
  let queryStr = filter.own_sort ? `&own_sort=${filter.own_sort}` : ''
  queryStr = filter.search ? `${queryStr}&search=${filter.search}` : queryStr
  return `${url}${queryStr}`
})

const listFiltering = (payload: filter) => {
  dataFilter.value = payload
  if (project.value)
    siteStore.fetchSiteOwnerList(project.value, payload.page, payload.own_sort, payload.search)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  if (project.value) siteStore.fetchSiteOwnerList(project.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: SiteOwner & filter) => siteStore.createSiteOwner(payload)

const onUpdate = (payload: SiteOwner & filter) => siteStore.updateSiteOwner(payload)

const relationPatch = (payload: Relation) => {
  const { page, own_sort, search } = dataFilter.value
  if (project.value) {
    const data = { project: project.value, page, own_sort, search, ...payload }
    siteStore.patchRelation(data)
  }
}

const multiSubmit = (payload: SiteOwner) => {
  const { page, own_sort, search } = dataFilter.value
  const submitData = { ...payload, page, own_sort, search }
  if (payload.pk) onUpdate(submitData)
  else onCreate(submitData)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSiteOwner(pk, project)
}

const dataSetup = (pk: number) => {
  siteStore.fetchAllSites(pk)
  siteStore.fetchSiteOwnerList(pk)
}

const dataReset = () => {
  siteStore.siteOwnerList = []
  siteStore.siteOwnerCount = 0
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
        @list-filtering="listFiltering"
      />
      <AddSiteOwner
        v-if="write_project_site"
        :project="project as number"
        @multi-submit="multiSubmit"
      />
      <TableTitleRow title="부지 소유자 목록" excel :url="excelUrl" :disabled="!project">
        <span v-if="project" class="pt-1 text-success">
          소유자 면적 :
          {{ numFormat(getOwnersTotal as number, 2) }}m<sup>2</sup> ({{
            numFormat((getOwnersTotal as number) * 0.3025, 2)
          }}평) 등록
        </span>
      </TableTitleRow>
      <SiteOwnerList
        :is-returned="isReturned"
        @page-select="pageSelect"
        @relation-patch="relationPatch"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>
  </ContentBody>
</template>
