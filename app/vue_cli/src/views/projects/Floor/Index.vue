<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { UnitFloorType } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import FloorAddForm from '@/views/projects/Floor/components/FloorAddForm.vue'
import FloorFormList from '@/views/projects/Floor/components/FloorFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pDataStore = useProjectData()
const fetchFloorTypeList = (projId: number) => pDataStore.fetchFloorTypeList(projId)
const createFloorType = (payload: UnitFloorType) => pDataStore.createFloorType(payload)
const updateFloorType = (payload: UnitFloorType) => pDataStore.updateFloorType(payload)
const deleteFloorType = (pk: number, project: number) => pDataStore.deleteFloorType(pk, project)

const onSubmit = (payload: UnitFloorType) =>
  createFloorType({ ...{ project: project.value }, ...payload })

const onUpdateFloor = (payload: UnitFloorType) =>
  updateFloorType({ ...{ project: project.value }, ...payload })

const onDeleteFloor = (pk: number) => {
  if (project.value) deleteFloorType(pk, project.value)
}

const projSelect = (target: number | null) => {
  pDataStore.floorTypeList = []
  if (!!target) fetchFloorTypeList(target)
}

onBeforeMount(() => fetchFloorTypeList(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <FloorAddForm :disabled="!project" @on-submit="onSubmit" />
      <FloorFormList @on-update="onUpdateFloor" @on-delete="onDeleteFloor" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
