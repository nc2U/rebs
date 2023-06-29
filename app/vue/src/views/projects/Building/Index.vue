<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { BuildingUnit } from '@/store/types/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BuildingAddForm from '@/views/projects/Building/components/BuildingAddForm.vue'
import BuildingFormList from '@/views/projects/Building/components/BuildingFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk || projStore.initProjId)

const pDataStore = useProjectData()
const fetchBuildingList = (projId: number) =>
  pDataStore.fetchBuildingList(projId)
const createBuilding = (payload: BuildingUnit) =>
  pDataStore.createBuilding(payload)
const updateBuilding = (payload: BuildingUnit) =>
  pDataStore.updateBuilding(payload)
const deleteBuilding = (pk: number, projId: number) =>
  pDataStore.deleteBuilding(pk, projId)

const onSelectAdd = (target: number) => {
  if (!!target) fetchBuildingList(target)
  else pDataStore.buildingList = []
}

const onCreateBuilding = (payload: BuildingUnit) =>
  createBuilding({ ...{ project: project.value }, ...payload })

const onUpdateBuilding = (payload: BuildingUnit) =>
  updateBuilding({ ...{ project: project.value }, ...payload })

const onDeleteBuilding = (pk: number) => {
  if (project.value) deleteBuilding(pk, project.value)
}

onBeforeMount(() => fetchBuildingList(project.value))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingAddForm :disabled="!project" @on-submit="onCreateBuilding" />
      <BuildingFormList
        @on-update="onUpdateBuilding"
        @on-delete="onDeleteBuilding"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
