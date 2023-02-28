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
const allAccD1List = computed(() =>
  proCashStore.allAccD1List.filter(d1 => d1.acc === '비용' && d1.code < '400'),
)
const allAccD2List = computed(() =>
  proCashStore.allAccD2List.filter(d2 => d2.code > '300' && d2.code < '400'),
)

const contStore = useContract()
const getOrderGroups = computed(() => contStore.getOrderGroups)

const proDataStore = useProjectData()
const getTypes = computed(() => proDataStore.getTypes)

provide('d1List', allAccD1List)
provide('d2List', allAccD2List)
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

const fetchProAllAccD1List = () => proCashStore.fetchProAllAccD1List()
const fetchProAllAccD2List = () => proCashStore.fetchProAllAccD2List()

const fetchOrderGroupList = (proj: number) =>
  contStore.fetchOrderGroupList(proj)

const fetchTypeList = (proj: number) => proDataStore.fetchTypeList(proj)

const onSubmit = (payload: ProOutBudget) =>
  createOutBudget({ ...{ project: project.value }, ...payload })

const onUpdateBudget = (payload: ProOutBudget) =>
  updateOutBudget({ ...{ project: project.value }, ...payload })

const onDeleteBudget = (pk: number) => deleteOutBudget(pk, project.value)

onBeforeMount(() => {
  fetchProAllAccD1List()
  fetchProAllAccD2List()
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)
  fetchOutBudgetList(initProjId.value)
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
