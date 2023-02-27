<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { ProIncBudget } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BudgetAddForm from '@/views/projects/IncBudget/components/BudgetAddForm.vue'
import BudgetFormList from '@/views/projects/IncBudget/components/BudgetFormList.vue'

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const onSelectAdd = (target: number) => {
  if (!!target) fetchIncBudgetList(target)
  else projectStore.proIncBudgetList = []
}

const fetchIncBudgetList = (pj: number) => projectStore.fetchIncBudgetList(pj)
const createIncBudget = (payload: ProIncBudget) =>
  projectStore.createIncBudget(payload)
const updateIncBudget = (payload: ProIncBudget) =>
  projectStore.updateIncBudget(payload)
const deleteIncBudget = (pk: number, project: number) =>
  projectStore.deleteIncBudget(pk, project)

const onSubmit = (payload: ProIncBudget) =>
  createIncBudget({ ...{ project: project.value }, ...payload })

const onUpdateBudget = (payload: ProIncBudget) =>
  updateIncBudget({ ...{ project: project.value }, ...payload })

const onDeleteBudget = (pk: number) => deleteIncBudget(pk, project.value)

onBeforeMount(() => fetchIncBudgetList(initProjId.value))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <BudgetAddForm :disabled="!project" @on-submit="onSubmit" />
      <BudgetFormList @on-update="onUpdateBudget" @on-delete="onDeleteBudget" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
