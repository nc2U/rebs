<script lang="ts" setup>
import { computed, onBeforeMount, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProCash } from '@/store/pinia/proCash'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { ProOutBudget } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BudgetAddForm from '@/views/projects/OutBudget/components/BudgetAddForm.vue'
import BudgetFormList from '@/views/projects/OutBudget/components/BudgetFormList.vue'

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const proCashStore = useProCash()
const allAccD2List = computed(() =>
  proCashStore.allAccD2List.filter(d2 => d2.acc === '비용' && d2.code < '400'),
)
const allAccD3List = computed(() =>
  proCashStore.allAccD3List.filter(d3 => d3.code > '300' && d3.code < '400'),
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
    fetchOutBudgetList(target)
  } else {
    contStore.orderGroupList = []
    proDataStore.unitTypeList = []
    projectStore.proOutBudgetList = []
  }
}

const fetchOutBudgetList = (pj: number) => projectStore.fetchOutBudgetList(pj)
const createOutBudget = (payload: ProOutBudget) =>
  projectStore.createOutBudget(payload)
const updateOutBudget = (payload: ProOutBudget) =>
  projectStore.updateOutBudget(payload)
const deleteOutBudget = (pk: number, project: number) =>
  projectStore.deleteOutBudget(pk, project)

const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List()
const fetchProAllAccD3List = () => proCashStore.fetchProAllAccD3List()

const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)

const fetchTypeList = (proj: number) => proDataStore.fetchTypeList(proj)

const onSubmit = (payload: ProOutBudget) => {
  if (project.value)
    createOutBudget({ ...{ project: project.value }, ...payload })
}

const onUpdateBudget = (payload: ProOutBudget) => {
  if (project.value)
    updateOutBudget({ ...{ project: project.value }, ...payload })
}

const onDeleteBudget = (pk: number) => {
  if (project.value) deleteOutBudget(pk, project.value)
}

onBeforeMount(() => {
  fetchProAllAccD2List()
  fetchProAllAccD3List()
  fetchOrderGroupList(project.value)
  fetchTypeList(project.value)
  fetchOutBudgetList(project.value)
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
