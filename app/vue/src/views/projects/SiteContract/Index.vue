<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { SiteContract } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddSiteContract from './components/AddSiteContract.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SiteContractList from './components/SiteContractList.vue'

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
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const siteStore = useSite()
const getContsTotal = computed(() => siteStore.getContsTotal?.contracted_area)

const onSelectAdd = (target: number) => {
  if (!!target) {
    siteStore.fetchAllOwners(target)
    siteStore.fetchSiteContList(target)
  } else {
    siteStore.siteContList = []
    siteStore.siteContCount = 0
  }
}

const listFiltering = (payload: filter) => {
  dataFilter.value = payload
  if (project.value)
    siteStore.fetchSiteContList(
      project.value,
      payload.page,
      payload.own_sort,
      payload.search,
    )
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  if (project.value) siteStore.fetchSiteContList(project.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: SiteContract) => siteStore.createSiteCont(payload)

const onUpdate = (payload: SiteContract) => siteStore.updateSiteCont(payload)

const multiSubmit = (payload: SiteContract) => {
  if (payload.pk) onUpdate(payload)
  else onCreate(payload)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSiteCont(pk, project)
}

const excelUrl = 'excel/sites-contracts/?project=' + project.value

onBeforeMount(() => {
  if (initProjId.value) {
    siteStore.fetchAllOwners(initProjId.value)
    siteStore.fetchSiteContList(initProjId.value)
  }
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
      <AddSiteContract :project="project" @multi-submit="multiSubmit" />
      <TableTitleRow title="부지 매입계약 목록" excel :url="excelUrl">
        <span class="pt-1 text-success">
          총 계약 면적 : {{ numFormat(getContsTotal, 2) }}m<sup>2</sup> ({{
            numFormat(getContsTotal * 0.3025, 2)
          }}
          평) 등록
        </span>
      </TableTitleRow>
      <SiteContractList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
