<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { Relation, SiteOwner } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
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

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const isReturned = computed(() => projectStore.project?.is_returned_area)

const siteStore = useSite()
const getOwnersTotal = computed(() => siteStore.getOwnersTotal?.owned_area)

const onSelectAdd = (target: number) => {
  if (!!target) {
    siteStore.fetchAllSites(target)
    siteStore.fetchSiteOwnerList(target)
  } else {
    siteStore.siteOwnerList = []
    siteStore.siteOwnerCount = 0
  }
}

const listFiltering = (payload: filter) => {
  dataFilter.value = payload
  siteStore.fetchSiteOwnerList(
    project.value || initProjId.value,
    payload.page,
    payload.own_sort,
    payload.search,
  )
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  siteStore.fetchSiteOwnerList(project.value || initProjId.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: SiteOwner & filter) =>
  siteStore.createSiteOwner(payload)

const onUpdate = (payload: SiteOwner & filter) =>
  siteStore.updateSiteOwner(payload)

const relationPatch = (payload: Relation) => {
  const { page, own_sort, search } = dataFilter.value
  const data = { project: project.value, page, own_sort, search, ...payload }
  siteStore.patchRelation(data)
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

const excelUrl = 'excel/sites-by-owner/?project=' + project.value

onBeforeMount(() => {
  siteStore.fetchAllSites(initProjId.value)
  siteStore.fetchSiteOwnerList(initProjId.value)
})
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
        @list-filtering="listFiltering"
      />
      <AddSiteOwner :project="project" @multi-submit="multiSubmit" />
      <TableTitleRow title="부지 소유자 목록" excel :url="excelUrl">
        <span class="pt-1 text-success">
          소유자 면적 : {{ numFormat(getOwnersTotal, 2) }}m<sup>2</sup> ({{
            numFormat(getOwnersTotal * 0.3025, 2)
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

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
