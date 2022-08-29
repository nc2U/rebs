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
  search: '',
})

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const isReturned = computed(() => projectStore.project?.is_returned_area)

const siteStore = useSite()

const onSelectAdd = (target: any) => {
  if (!!target) {
    siteStore.fetchSiteOwnerList(target)
  } else {
    siteStore.siteOwnerList = []
  }
}

const listFiltering = (payload: any) => {
  dataFilter.value = payload
  siteStore.fetchSiteOwnerList(project.value, payload.page, payload.search)
}

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  siteStore.fetchSiteOwnerList(project.value, page)
  listControl.value.listFiltering(page)
}

const onCreate = (payload: any) => siteStore.createSiteOwner(payload)

const onUpdate = (payload: any) => siteStore.updateSiteOwner(payload)

const multiSubmit = (payload: any) => {
  if (payload.pk) onUpdate(payload)
  else onCreate(payload)
}

const onDelete = (payload: { pk: number; project: number }) => {
  const { pk, project } = payload
  siteStore.deleteSiteOwner(pk, project)
}

onBeforeMount(() => {
  siteStore.fetchSiteOwnerList(initProjId.value)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController @list-filtering="listFiltering" />
      <AddSiteOwner @multi-submit="multiSubmit" />
      <SiteOwnerList
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
