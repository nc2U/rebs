<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { UnitFilter, useContract } from '@/store/pinia/contract'
import { Contract } from '@/store/types/contract'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractForm from './components/ContractForm.vue'

const contForm = ref()

const [route, router] = [useRoute(), useRouter()]

const contractStore = useContract()
const contract = computed(() => contractStore.contract)

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
const unitSet = computed(() => projectStore.project?.is_unit_set)
const isUnion = computed(() => !projectStore.project?.is_direct_manage)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)

const fetchContractor = (contor: number) =>
  contractStore.fetchContractor(contor)

const fetchOrderGroupList = (projId: number) =>
  contractStore.fetchOrderGroupList(projId)

const fetchKeyUnitList = (payload: UnitFilter) =>
  contractStore.fetchKeyUnitList(payload)

const fetchHouseUnitList = (payload: UnitFilter) =>
  contractStore.fetchHouseUnitList(payload)

const projectDataStore = useProjectData()
const fetchTypeList = (projId: number) => projectDataStore.fetchTypeList(projId)

const proCashStore = useProCash()
const fetchAllProBankAccList = (projId: number) =>
  proCashStore.fetchAllProBankAccList(projId)

const paymentStore = usePayment()
const fetchPayOrderList = (projId: number) =>
  paymentStore.fetchPayOrderList(projId)

watch(contract, newVal => {
  if (newVal && project.value) {
    fetchKeyUnitList({
      project: project.value,
      unit_type: newVal.unit_type,
      contract: newVal.pk,
      available: 'false',
    })
    if (newVal.keyunit?.houseunit) {
      fetchHouseUnitList({
        project: project.value,
        unit_type: newVal.unit_type,
        contract: newVal.pk,
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
    fetchAllProBankAccList(target)
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

const getContract = (contor: string) =>
  fetchContractor(parseInt(contor)).then(res => fetchContract(res.contract))

const typeSelect = (type: number) => {
  const unit_type = type
  if (project.value) {
    fetchKeyUnitList({ project: project.value, unit_type })
    fetchHouseUnitList({ project: project.value, unit_type })
  }
}

const onCreate = (payload: Contract) => {
  if (project.value) payload.project = project.value
  contractStore.createContractSet({ ...payload })
  router.replace({ name: '계약 내역 조회' })
}

const onUpdate = (payload: Contract) => {
  if (project.value) payload.project = project.value
  contractStore.updateContractSet({ ...payload })
}

onBeforeMount(() => {
  if (initProjId.value) {
    fetchOrderGroupList(initProjId.value)
    fetchTypeList(initProjId.value)
    fetchAllProBankAccList(initProjId.value)
    fetchPayOrderList(initProjId.value)
    fetchKeyUnitList({ project: initProjId.value })
    fetchHouseUnitList({ project: initProjId.value })
  }

  if (route.query.contractor) {
    getContract(route.query.contractor as string)
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
      :project="project"
      :contract="contract"
      :unit-set="unitSet"
      :is-union="isUnion"
      @type-select="typeSelect"
      @on-create="onCreate"
      @on-update="onUpdate"
    />
  </ContentBody>
</template>
