<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { UnitFloorType } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import FloorAddForm from '@/views/projects/Floor/components/FloorAddForm.vue'
import FloorFormList from '@/views/projects/Floor/components/FloorFormList.vue'

const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const projectDataStore = useProjectData()
const fetchFloorTypeList = (projId: number) =>
  projectDataStore.fetchFloorTypeList(projId)
const createFloorType = (payload: UnitFloorType) =>
  projectDataStore.createFloorType(payload)
const updateFloorType = (payload: UnitFloorType) =>
  projectDataStore.updateFloorType(payload)
const deleteFloorType = (pk: number, project: number) =>
  projectDataStore.deleteFloorType(pk, project)

const onSelectAdd = (target: number) => {
  if (!!target) fetchFloorTypeList(target)
  else projectDataStore.floorTypeList = []
}

const onSubmit = (payload: UnitFloorType) =>
  createFloorType({ ...{ project: project.value }, ...payload })

const onUpdateFloor = (payload: UnitFloorType) =>
  updateFloorType({ ...{ project: project.value }, ...payload })

const onDeleteFloor = (pk: number) => deleteFloorType(pk, project.value)

onBeforeMount(() => fetchFloorTypeList(initProjId.value))
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
