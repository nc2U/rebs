<script lang="ts" setup>
import { computed, onBeforeMount, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { type UnitType } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import TypeAddForm from '@/views/projects/Type/components/TypeAddForm.vue'
import TypeFormList from '@/views/projects/Type/components/TypeFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const typeSort = [
  { value: '1', label: '공동주택' },
  { value: '2', label: '오피스텔' },
  { value: '3', label: '숙박시설' },
  { value: '4', label: '지식산업센터' },
  { value: '5', label: '근린생활시설' },
  { value: '6', label: '기타' },
]

provide('typeSort', typeSort)

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
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <TypeAddForm :disabled="!project" @on-submit="onSubmit" />
      <TypeFormList @on-update="onUpdateType" @on-delete="onDeleteType" />
    </CCardBody>
  </ContentBody>
</template>
