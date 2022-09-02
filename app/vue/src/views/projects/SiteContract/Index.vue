<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddSite from './components/AddSite.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SiteContractList from './components/SiteContractList.vue'

const listControl = ref()

const dataFilter = ref({
  page: 1,
  own_sort: '',
  search: '',
})

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const siteStore = useSite()

const onSelectAdd = (target: any) => {
  if (!!target) {
    siteStore.fetchSiteContList(target)
  } else {
    siteStore.siteContList = []
    siteStore.siteContCount = 0
  }
}

const listFiltering = (payload: any) => {
  dataFilter.value = payload
  siteStore.fetchSiteContList(
    project.value || initProjId.value,
    payload.page,
    payload.own_sort,
    payload.search,
  )
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  siteStore.fetchSiteContList(project.value || initProjId.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: any) => siteStore.createSiteCont(payload)

const onUpdate = (payload: any) => siteStore.updateSiteCont(payload)

const multiSubmit = (payload: any) => {
  if (payload.pk) onUpdate(payload)
  else onCreate(payload)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSiteCont(pk, project)
}

onBeforeMount(() => {
  siteStore.fetchSiteContList(initProjId.value)
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
      <AddSite :project="project" @multi-submit="multiSubmit" />
      <TableTitleRow title="부지 매입계약 목록" excel url="" disabled />
      <SiteContractList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
