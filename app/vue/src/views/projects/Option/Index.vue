<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { type UnitType } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OptionAddForm from '@/views/projects/Option/components/OptionAddForm.vue'
import OptionFormList from '@/views/projects/Option/components/OptionFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pDataStore = useProjectData()
const fetchTypeList = (projId: number) => pDataStore.fetchTypeList(projId)
const createType = (payload: UnitType) => pDataStore.createType(payload)
const updateType = (payload: UnitType) => pDataStore.updateType(payload)
const deleteType = (pk: number, project: number) => pDataStore.deleteType(pk, project)

const onSubmit = (payload: UnitType) => createType({ ...{ project: project.value }, ...payload })
const onUpdateType = (payload: UnitType) =>
  updateType({ ...{ project: project.value }, ...payload })
const onDeleteType = (pk: number) => {
  if (project.value) deleteType(pk, project.value)
}

const projSelect = (target: number | null) => {
  pDataStore.unitTypeList = []
  if (!!target) fetchTypeList(target)
}

onBeforeMount(() => fetchTypeList(project.value || projStore.initProjId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="ProjectSelect"
    @proj-select="projSelect"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <OptionAddForm :disabled="!project" @on-submit="onSubmit" />
      <OptionFormList @on-update="onUpdateType" @on-delete="onDeleteType" />
    </CCardBody>
  </ContentBody>
</template>
