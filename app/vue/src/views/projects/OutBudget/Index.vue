<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { ProOutBudget } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BudgetAddForm from '@/views/projects/OutBudget/components/BudgetAddForm.vue'
import BudgetFormList from '@/views/projects/OutBudget/components/BudgetFormList.vue'

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const onSelectAdd = (target: number) => {
  if (!!target) fetchOutBudgetList(target)
  else projectStore.proOutBudgetList = []
}

const fetchOutBudgetList = (pj: number) => projectStore.fetchOutBudgetList(pj)
const createOutBudget = (payload: ProOutBudget) =>
  projectStore.createOutBudget(payload)
const updateOutBudget = (payload: ProOutBudget) =>
  projectStore.updateOutBudget(payload)
const deleteOutBudget = (pk: number, project: number) =>
  projectStore.deleteOutBudget(pk, project)

const onSubmit = (payload: ProOutBudget) =>
  createOutBudget({ ...{ project: project.value }, ...payload })

const onUpdateBudget = (payload: ProOutBudget) =>
  updateOutBudget({ ...{ project: project.value }, ...payload })

const onDeleteBudget = (pk: number) => deleteOutBudget(pk, project.value)

onBeforeMount(() => fetchOutBudgetList(initProjId.value))
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
