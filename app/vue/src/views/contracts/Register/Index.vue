<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { UnitFilter, useContract } from '@/store/pinia/contract'
import { Contract } from '@/store/types/contract'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractForm from '@/views/contracts/Register/components/ContractForm.vue'

const contForm = ref()

const [route, router] = [useRoute(), useRouter()]

const contractStore = useContract()
const contract = computed(() => contractStore.contract)

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)
const unitSet = computed(() => projectStore.project?.is_unit_set)
const isUnion = computed(() => !projectStore.project?.is_direct_manage)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)

const fetchOrderGroupList = (projId: number) =>
  contractStore.fetchOrderGroupList(projId)

const fetchKeyUnitList = (payload: UnitFilter) =>
  contractStore.fetchKeyUnitList(payload)

const fetchHouseUnitList = (payload: UnitFilter) =>
  contractStore.fetchHouseUnitList(payload)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

const proCashStore = useProCash()
const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)

const paymentStore = usePayment()
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)

watch(contract, newVal => {
  if (newVal) {
    fetchKeyUnitList({
      project: project.value,
      unit_type: newVal.unit_type,
      contract: route.query.contract as string,
      available: 'false',
    })
    if (newVal.keyunit?.houseunit) {
      fetchHouseUnitList({
        project: project.value,
        unit_type: newVal.unit_type,
        contract: route.query.contract as string,
      })
    } else {
      fetchHouseUnitList({
        project: project.value,
        unit_type: newVal.unit_type,
      })
    }
  }
})

const onSelectAdd = (target: number) => {
  contForm.value.formReset()

  if (!!target) {
    fetchOrderGroupList(target)
    fetchKeyUnitList({ project: target })
    fetchHouseUnitList({ project: target })
    fetchTypeList(target)
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  } else {
    contractStore.contract = null
    contractStore.orderGroupList = []
    contractStore.keyUnitList = []
    contractStore.houseUnitList = []

    projectDataStore.unitTypeList = []
    paymentStore.payOrderList = []
    proCashStore.proBankAccountList = []
  }
}

const getContract = (cont: string) => fetchContract(parseInt(cont))

const typeSelect = (type: number) => {
  const unit_type = type
  fetchKeyUnitList({ project: project.value, unit_type })
  fetchHouseUnitList({ project: project.value, unit_type })
}

const onCreate = (payload: Contract) => {
  payload.project = project.value
  contractStore.createContractSet({ ...payload })
  router.replace({ name: '계약내역 조회' })
}

const onUpdate = (payload: Contract) => {
  payload.project = project.value
  contractStore.updateContractSet({ ...payload })
}

onBeforeMount(() => {
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)

  fetchProBankAccList(initProjId.value)
  fetchPayOrderList(initProjId.value)

  fetchKeyUnitList({ project: initProjId.value })
  fetchHouseUnitList({ project: initProjId.value })

  if (route.query.contract) {
    getContract(route.query.contract as string)
  }
})

onBeforeRouteLeave(() => {
  contractStore.contract = null
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <ContractForm
      ref="contForm"
      :contract="contract"
      :unit-set="unitSet"
      :is-union="isUnion"
      @type-select="typeSelect"
      @on-create="onCreate"
      @on-update="onUpdate"
    />
  </ContentBody>
</template>
