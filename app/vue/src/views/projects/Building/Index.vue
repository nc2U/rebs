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

const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const projectDataStore = useProjectData()
const fetchBuildingList = (projId: number) =>
  projectDataStore.fetchBuildingList(projId)
const createBuilding = (payload: BuildingUnit) =>
  projectDataStore.createBuilding(payload)
const updateBuilding = (payload: BuildingUnit) =>
  projectDataStore.updateBuilding(payload)
const deleteBuilding = (pk: number, projId: number) =>
  projectDataStore.deleteBuilding(pk, projId)

onBeforeMount(() => fetchBuildingList(initProjId.value))

const onSelectAdd = (target: number) => {
  if (!!target) fetchBuildingList(target)
  else projectDataStore.buildingList = []
}

const onCreateBuilding = (payload: BuildingUnit) =>
  createBuilding({ ...{ project: project.value }, ...payload })

const onUpdateBuilding = (payload: BuildingUnit) =>
  updateBuilding({ ...{ project: project.value }, ...payload })

const onDeleteBuilding = (pk: number) => deleteBuilding(pk, project.value)
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
