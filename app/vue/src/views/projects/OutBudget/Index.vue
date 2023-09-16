<script lang="ts" setup>
import { computed, onBeforeMount, provide } from 'vue'
import { pageTitle, navMenu } from '@/views/projects/_menu/headermixin1'
import { useProject } from '@/store/pinia/project'
import { useProCash } from '@/store/pinia/proCash'
import { useContract } from '@/store/pinia/contract'
import { useProjectData } from '@/store/pinia/project_data'
import { type ProOutBudget } from '@/store/types/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import BudgetAddForm from '@/views/projects/OutBudget/components/BudgetAddForm.vue'
import BudgetFormList from '@/views/projects/OutBudget/components/BudgetFormList.vue'

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const pCashStore = useProCash()
const allAccD2List = computed(() =>
  pCashStore.allAccD2List.filter(d2 => d2.d1 === '비용' && d2.code < '690'),
)
const allAccD3List = computed(() =>
  pCashStore.allAccD3List.filter(d3 => d3.code > '600' && d3.code < '690'),
)

const contStore = useContract()
const getOrderGroups = computed(() => contStore.getOrderGroups)

const pDataStore = useProjectData()
const getTypes = computed(() => pDataStore.getTypes)

provide('d2List', allAccD2List)
provide('d3List', allAccD3List)
provide('orderGroups', getOrderGroups)
provide('unitTypes', getTypes)

const fetchOutBudgetList = (pj: number) => projStore.fetchOutBudgetList(pj)
const createOutBudget = (payload: ProOutBudget) => projStore.createOutBudget(payload)
const updateOutBudget = (payload: ProOutBudget) => projStore.updateOutBudget(payload)
const deleteOutBudget = (pk: number, project: number) => projStore.deleteOutBudget(pk, project)

const fetchProAllAccD2List = () => pCashStore.fetchProAllAccD2List()
const fetchProAllAccD3List = () => pCashStore.fetchProAllAccD3List()

const fetchOrderGroupList = (proj: number) => contStore.fetchOrderGroupList(proj)

const fetchTypeList = (proj: number) => pDataStore.fetchTypeList(proj)

const onSubmit = (payload: ProOutBudget) => {
  if (project.value) createOutBudget({ ...{ project: project.value }, ...payload })
}

const onUpdateBudget = (payload: ProOutBudget) => {
  if (project.value) updateOutBudget({ ...{ project: project.value }, ...payload })
}

const onDeleteBudget = (pk: number) => {
  if (project.value) deleteOutBudget(pk, project.value)
}

const dataSetup = (pk: number) => {
  fetchOrderGroupList(pk)
  fetchTypeList(pk)
  fetchOutBudgetList(pk)
}

const dataReset = () => {
  contStore.orderGroupList = []
  pDataStore.unitTypeList = []
  projStore.proOutBudgetList = []
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onBeforeMount(() => {
  fetchProAllAccD2List()
  fetchProAllAccD3List()
  dataSetup(project.value || projStore.initProjId)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" @proj-select="projSelect" />

  <ContentBody>
    <CCardBody class="pb-5">
      <BudgetAddForm :disabled="!project" @on-submit="onSubmit" />
      <BudgetFormList @on-update="onUpdateBudget" @on-delete="onDeleteBudget" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
