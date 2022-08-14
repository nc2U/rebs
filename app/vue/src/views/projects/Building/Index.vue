<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BuildingAddForm from '@/views/projects/Building/components/BuildingAddForm.vue'
import BuildingFormList from '@/views/projects/Building/components/BuildingFormList.vue'

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const fetchBuildingList = (projId: number) =>
  store.dispatch('project/fetchBuildingList', projId)
const createBuilding = (payload: any) =>
  store.dispatch('project/createBuilding', payload)
const updateBuilding = (payload: any) =>
  store.dispatch('project/updateBuilding', payload)
const deleteBuilding = (payload: any) =>
  store.dispatch('project/deleteBuilding', payload)

onBeforeMount(() => fetchBuildingList(initProjId.value))

const onSelectAdd = (target: any) => {
  if (target !== '') fetchBuildingList(target)
  else store.commit('project/updateState', { buildingList: [] })
}
const onSubmit = (payload: any) =>
  createBuilding({ ...{ project: project.value }, ...payload })

const onUpdateBuilding = (payload: any) =>
  updateBuilding({ ...{ project: project.value }, ...payload })

const onDeleteBuilding = (pk: number) =>
  deleteBuilding({ ...{ pk }, ...{ project: project.value } })
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingAddForm :disabled="!project" @on-submit="onSubmit" />
      <BuildingFormList
        @on-update="onUpdateBuilding"
        @on-delete="onDeleteBuilding"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
