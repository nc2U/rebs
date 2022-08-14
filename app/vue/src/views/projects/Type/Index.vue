<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import TypeAddForm from '@/views/projects/Type/components/TypeAddForm.vue'
import TypeFormList from '@/views/projects/Type/components/TypeFormList.vue'

const store = useStore()
const projectStore = useProject()

const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)
const createType = (payload: any) =>
  store.dispatch('project/createType', payload)
const updateType = (payload: any) =>
  store.dispatch('project/updateType', payload)
const deleteType = (payload: any) =>
  store.dispatch('project/deleteType', payload)

const onSelectAdd = (target: any) => {
  if (target !== '') fetchTypeList(target)
  else store.commit('project/updateState', { unitTypeList: [] })
}
const onSubmit = (payload: any) =>
  createType({ ...{ project: project.value }, ...payload })
const onUpdateType = (payload: any) =>
  updateType({ ...{ project: project.value }, ...payload })
const onDeleteType = (pk: number) =>
  deleteType({ ...{ pk }, ...{ project: project.value } })

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
