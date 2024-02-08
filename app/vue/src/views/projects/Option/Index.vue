<script lang="ts" setup>
import { computed, onBeforeMount, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import type { OptionItem } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import OptionAddForm from '@/views/projects/Option/components/OptionAddForm.vue'
import OptionFormList from '@/views/projects/Option/components/OptionFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pDataStore = useProjectData()
const getTypes = computed(() => pDataStore.getTypes)
provide('getTypes', getTypes)

const fetchTypeList = (projId: number, sort?: '1') => pDataStore.fetchTypeList(projId, sort)
const fetchOptionItemList = (proj: number) => pDataStore.fetchOptionItemList(proj)
const createOptionItem = (payload: OptionItem) => pDataStore.createOptionItem(payload)
const updateOptionItem = (payload: OptionItem) => pDataStore.updateOptionItem(payload)
const deleteOptionItem = (pk: number, proj: number) => pDataStore.deleteOptionItem(pk, proj)

const onSubmit = (payload: OptionItem) =>
  createOptionItem({ ...{ project: project.value }, ...payload })

const onUpdateOption = (payload: OptionItem) =>
  updateOptionItem({ ...{ project: project.value }, ...payload })

const onDeleteOption = (pk: number) => {
  if (project.value) deleteOptionItem(pk, project.value)
}

const projSelect = (target: number | null) => {
  pDataStore.unitTypeList = []
  if (!!target) fetchTypeList(target)
}

onBeforeMount(() => {
  fetchTypeList(project.value ?? projStore.initProjId, '1')
  fetchOptionItemList(project.value ?? projStore.initProjId)
})
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
      <OptionAddForm :disabled="!project" :get-types="getTypes" @on-submit="onSubmit" />
      <OptionFormList @on-update="onUpdateOption" @on-delete="onDeleteOption" />
    </CCardBody>
  </ContentBody>
</template>
