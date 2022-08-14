<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import FloorAddForm from '@/views/projects/Floor/components/FloorAddForm.vue'
import FloorFormList from '@/views/projects/Floor/components/FloorFormList.vue'

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const fetchFloorTypeList = (projId: number) =>
  store.dispatch('project/fetchFloorTypeList', projId)
const createFloorType = (payload: any) =>
  store.dispatch('project/createFloorType', payload)
const updateFloorType = (payload: any) =>
  store.dispatch('project/updateFloorType', payload)
const deleteFloorType = (payload: any) =>
  store.dispatch('project/deleteFloorType', payload)

onBeforeMount(() => fetchFloorTypeList(initProjId.value))

const onSelectAdd = (target: any) => {
  if (target !== '') fetchFloorTypeList(target)
  else store.commit('project/updateState', { floorTypeList: [] })
}
const onSubmit = (payload: any) => {
  createFloorType({ ...{ project: project.value }, ...payload })
}
const onUpdateFloor = (payload: any) => {
  updateFloorType({ ...{ project: project.value }, ...payload })
}
const onDeleteFloor = (pk: number) => {
  deleteFloorType({ ...{ pk }, ...{ project: project.value } })
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <FloorAddForm :disabled="!project" @on-submit="onSubmit" />
      <FloorFormList @on-update="onUpdateFloor" @on-delete="onDeleteFloor" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
