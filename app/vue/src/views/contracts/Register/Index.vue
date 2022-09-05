<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useContract } from '@/store/pinia/contract'
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
const project = computed(() => projectStore.project)
const initProjId = computed(() => projectStore.initProjId)
const unitSet = computed(() => project.value?.is_unit_set)
const isUnion = computed(() => !project.value?.is_direct_manage)

const fetchContract = (cont: any) => contractStore.fetchContract(cont)

const fetchOrderGroupList = (projId: number) =>
  contractStore.fetchOrderGroupList(projId)

const fetchKeyUnitList = (payload: any) =>
  contractStore.fetchKeyUnitList(payload)

const fetchHouseUnitList = (payload: any) =>
  contractStore.fetchHouseUnitList(payload)

const createContractSet = (payload: any) => console.log(payload) // contractStore.createContractSet(payload)
const updateContractSet = (payload: any) => console.log(payload) // contractStore.updateContractSet(payload)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

const proCashStore = useProCash()
const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)

const paymentStore = usePayment()
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)

watch(contract, newVal => {
  const projId = project.value?.pk || initProjId.value
  if (newVal) {
    fetchKeyUnitList({
      project: projId,
      unit_type: newVal.unit_type,
      contract: route.query.contract,
      available: 'false',
    })
    if (newVal.keyunit?.houseunit) {
      fetchHouseUnitList({
        project: projId,
        unit_type: newVal.unit_type,
        contract: route.query.contract,
      })
    } else {
      fetchHouseUnitList({
        project: projId,
        unit_type: newVal.unit_type,
      })
    }
  }
})

const onSelectAdd = (target: any) => {
  contForm.value.formReset()

  if (!!target) {
    fetchOrderGroupList(target)
    fetchKeyUnitList({ project: target })
    fetchHouseUnitList({ project: target })
    fetchTypeList(target)
    fetchPayOrderList(target)
    fetchProBankAccList(target)
  } else {
    store.commit('contract/updateState', {
      contract: null,
      orderGroupList: [],
      keyUnitList: [],
      houseUnitList: [],
    })
    store.commit('project/updateState', { unitTypeList: [] })
    store.commit('payment/updateState', { payOrderList: [] })
    store.commit('proCash/updateState', { proBankAccountList: [] })
  }
}

const getContract = (cont: any) => fetchContract(cont)

const typeSelect = (type: number) => {
  const unit_type = type
  fetchKeyUnitList({ project: project.value?.pk, unit_type })
  fetchHouseUnitList({ project: project.value?.pk, unit_type })
}

const onCreate = (payload: any) => {
  createContractSet({ project: project.value?.pk, ...payload })
  router.push({ name: '계약내역 조회' })
}
const onUpdate = (payload: any) =>
  updateContractSet({ project: project.value?.pk, ...payload })

onBeforeMount(() => {
  fetchOrderGroupList(initProjId.value)
  fetchTypeList(initProjId.value)

  fetchProBankAccList(initProjId.value)
  fetchPayOrderList(initProjId.value)

  fetchKeyUnitList({ project: initProjId.value })
  fetchHouseUnitList({ project: initProjId.value })

  if (route.query.contract) {
    getContract(route.query.contract)
  }
})

onBeforeRouteLeave(() =>
  store.commit('contract/updateState', { contract: null }),
)
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
