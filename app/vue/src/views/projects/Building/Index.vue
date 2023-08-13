<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { type BuildingUnit } from '@/store/types/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BuildingAddForm from '@/views/projects/Building/components/BuildingAddForm.vue'
import BuildingFormList from '@/views/projects/Building/components/BuildingFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pDataStore = useProjectData()
const fetchBuildingList = (projId: number) => pDataStore.fetchBuildingList(projId)
const createBuilding = (payload: BuildingUnit) => pDataStore.createBuilding(payload)
const updateBuilding = (payload: BuildingUnit) => pDataStore.updateBuilding(payload)
const deleteBuilding = (pk: number, projId: number) => pDataStore.deleteBuilding(pk, projId)

const onCreateBuilding = (payload: BuildingUnit) =>
  createBuilding({ ...{ project: project.value }, ...payload })

const onUpdateBuilding = (payload: BuildingUnit) =>
  updateBuilding({ ...{ project: project.value }, ...payload })

const onDeleteBuilding = (pk: number) => {
  if (project.value) deleteBuilding(pk, project.value as number)
}

const projSelect = (target: number | null) => {
  pDataStore.buildingList = []
  if (!!target) fetchBuildingList(target)
}

onBeforeMount(() => fetchBuildingList(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <BuildingAddForm :disabled="!project" @on-submit="onCreateBuilding" />
      <BuildingFormList @on-update="onUpdateBuilding" @on-delete="onDeleteBuilding" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
