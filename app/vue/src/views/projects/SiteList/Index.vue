<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useSite } from '@/store/pinia/project_site'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin3'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
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

const onSelectAdd = (target: any) => {
  if (!!target) {
    siteStore.fetchSiteList(target)
  } else {
    siteStore.siteList = []
  }
}

const listFiltering = (payload: any) => {
  dataFilter.value = payload
  siteStore.fetchSiteList(project.value, payload.page, payload.search)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  siteStore.fetchSiteList(project.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: any) => {
  payload.project = project.value
  console.log(payload)
}

const onUpdate = (payload: any) => console.log(payload)

const multiSubmit = (payload: any) => {
  if (payload.pk) onCreate(payload)
  else onUpdate(payload)
}

const onDelete = (payload: any) => console.log(payload)

onBeforeMount(() => {
  siteStore.fetchSiteList(initProjId.value)
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
      <ListController @list-filtering="listFiltering" />
      <AddSite @multi-submit="multiSubmit" />
      <SiteList
        ref="listControl"
        :is-returned="isReturned"
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
