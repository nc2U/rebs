<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/projects/SiteOwner/components/ListController.vue'
import AddSiteOwner from '@/views/projects/SiteOwner/components/AddSiteOwner.vue'
import SiteOwnerList from '@/views/projects/SiteOwner/components/SiteOwnerList.vue'

const listControl = ref()

const dataFilter = ref({
  page: 1,
  own_sort: '',
  search: '',
})

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
const isReturned = computed(() => projectStore.project?.is_returned_area)

const siteStore = useSite()

const onSelectAdd = (target: any) => {
  if (!!target) {
    siteStore.fetchAllSites(target)
    siteStore.fetchSiteOwnerList(target)
  } else {
    siteStore.siteOwnerList = []
    siteStore.siteOwnerCount = 0
  }
}

const listFiltering = (payload: any) => {
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

const onCreate = (payload: any) => console.log(payload) // siteStore.createSiteOwner(payload)

const onUpdate = (payload: any) => console.log(payload) // siteStore.updateSiteOwner(payload)

const relationUpdate = (payload: any) => {
  const data = { project: project.value, ...payload }
  console.log(data)
  siteStore.updateRelation(data)
} // console.log('relation-update', payload)

const multiSubmit = (payload: any) => {
  if (payload.pk) onUpdate(payload)
  else onCreate(payload)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSiteOwner(pk, project)
}

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
      <SiteOwnerList
        :is-returned="isReturned"
        @page-select="pageSelect"
        @relation-update="relationUpdate"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
