<script lang="ts" setup>
import { computed, onBeforeMount, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProCash } from '@/store/pinia/proCash'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { ProIncBudget } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BudgetAddForm from '@/views/projects/IncBudget/components/BudgetAddForm.vue'
import BudgetFormList from '@/views/projects/IncBudget/components/BudgetFormList.vue'

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const proCashStore = useProCash()
const allAccD2List = computed(() =>
  proCashStore.allAccD2List.filter(d1 => d1.pk <= 2),
)
const allAccD3List = computed(() =>
  proCashStore.allAccD3List.filter(d3 => d3.pk <= 2),
)

const contStore = useContract()
const getOrderGroups = computed(() => contStore.getOrderGroups)

const proDataStore = useProjectData()
const getTypes = computed(() => proDataStore.getTypes)

provide('d1List', allAccD2List)
provide('d3List', allAccD3List)
provide('orderGroups', getOrderGroups)
provide('unitTypes', getTypes)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchOrderGroupList(target)
    fetchTypeList(target)
    fetchIncBudgetList(target)
  } else {
    contStore.orderGroupList = []
    proDataStore.unitTypeList = []
    projectStore.proIncBudgetList = []
  }
}

const fetchIncBudgetList = (pj: number) => projectStore.fetchIncBudgetList(pj)
const createIncBudget = (payload: ProIncBudget) =>
  projectStore.createIncBudget(payload)
const updateIncBudget = (payload: ProIncBudget) =>
  projectStore.updateIncBudget(payload)
const deleteIncBudget = (pk: number, project: number) =>
  projectStore.deleteIncBudget(pk, project)

const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List()
const fetchProAllAccD3List = () => proCashStore.fetchProAllAccD3List()

const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)

const fetchTypeList = (proj: number) => proDataStore.fetchTypeList(proj)

const onSubmit = (payload: ProIncBudget) => {
  if (project.value)
    createIncBudget({ ...{ project: project.value }, ...payload })
}

const onUpdateBudget = (payload: ProIncBudget) => {
  if (project.value)
    updateIncBudget({ ...{ project: project.value }, ...payload })
}

const onDeleteBudget = (pk: number) => {
  if (project.value) deleteIncBudget(pk, project.value)
}

onBeforeMount(() => {
  fetchProAllAccD2List()
  fetchProAllAccD3List()
  fetchOrderGroupList(project.value)
  fetchTypeList(project.value)
  fetchIncBudgetList(project.value)
})
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
