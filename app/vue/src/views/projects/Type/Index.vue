<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { UnitType } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import TypeAddForm from '@/views/projects/Type/components/TypeAddForm.vue'
import TypeFormList from '@/views/projects/Type/components/TypeFormList.vue'

const projectStore = useProject()

const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)
const createType = (payload: any) => projectDataStore.createType(payload)
const updateType = (payload: any) => projectDataStore.updateType(payload)
const deleteType = (pk: number, project: number) =>
  projectDataStore.deleteType(pk, project)

const onSelectAdd = (target: any) => {
  if (target !== '') fetchTypeList(target)
  else projectDataStore.unitTypeList = []
}
const onSubmit = (payload: UnitType) =>
  createType({ ...{ project: project.value }, ...payload })
const onUpdateType = (payload: UnitType) =>
  updateType({ ...{ project: project.value }, ...payload })
const onDeleteType = (pk: number) => deleteType(pk, project.value)

onBeforeMount(() => fetchTypeList(initProjId.value))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <TypeAddForm :disabled="!project" @on-submit="onSubmit" />
      <TypeFormList @on-update="onUpdateType" @on-delete="onDeleteType" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
