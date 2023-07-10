<script lang="ts" setup>
import { ref, computed, watch, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { UnitFilter, useContract } from '@/store/pinia/contract'
import { Contract } from '@/store/types/contract'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { usePayment } from '@/store/pinia/payment'
import { useProCash } from '@/store/pinia/proCash'
import { useRoute, useRouter } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractForm from './components/ContractForm.vue'

const contForm = ref()

const [route, router] = [useRoute(), useRouter()]

const contractStore = useContract()
const contract = computed(() => contractStore.contract)
const contractor = computed(() => contractStore.contractor)

const projStore = useProject()
const project = computed(() => projStore.project?.pk)
const unitSet = computed(() => projStore.project?.is_unit_set)
const isUnion = computed(() => !projStore.project?.is_direct_manage)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)

const fetchContractor = (contor: number, proj?: number) =>
  contractStore.fetchContractor(contor, proj)

const fetchContractorList = (projId: number, search = '') =>
  contractStore.fetchContractorList(projId, search)

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

watch(route, val => {
  const { contractor } = val.query
  if (!!contractor) getContract(contractor as string)
  else {
    contractStore.contract = null
    contractStore.contractor = null
  }
})

watch(contractor, val => {
  if (!!val)
    if (!!contract.value && contract.value.pk !== val.contract)
      fetchContract(val.contract)
})

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

const getContract = (contor: string) =>
  fetchContractor(Number(contor), project.value).then(res =>
    fetchContract(res.contract),
  )

const typeSelect = (payload: {
  unit_type?: number
  contract?: number
  available?: 'true' | ''
}) => {
  if (project.value) {
    fetchKeyUnitList({ project: project.value, ...payload })
    fetchHouseUnitList({ project: project.value, ...payload })
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

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

const dataSetup = (pk: number) => {
  fetchTypeList(pk)
  fetchPayOrderList(pk)
  fetchOrderGroupList(pk)
  fetchAllProBankAccList(pk)
  fetchKeyUnitList({ project: pk })
  fetchHouseUnitList({ project: pk })
}

const dataReset = () => {
  contractStore.contract = null
  contractStore.contractor = null
  contractStore.orderGroupList = []
  contractStore.keyUnitList = []
  contractStore.houseUnitList = []
  projectDataStore.unitTypeList = []
  paymentStore.payOrderList = []
  proCashStore.proBankAccountList = []
}

const projSelect = (target: number | null) => {
  dataReset()
  if (!!target) {
    contForm.value.formReset()
    dataSetup(target)
  }
}

onBeforeMount(() => {
  dataSetup(project.value || projStore.initProjId)

  if (route.query.contractor) getContract(route.query.contractor as string)
  else {
    contractStore.contract = null
    contractStore.contractor = null
  }
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @proj-select="projSelect"
  />

  <ContentBody>
    <ContractForm
      ref="contForm"
      :project="project"
      :contract="contract"
      :contractor="contractor"
      :unit-set="unitSet"
      :is-union="isUnion"
      @type-select="typeSelect"
      @on-create="onCreate"
      @on-update="onUpdate"
      @search-contractor="searchContractor"
    />
  </ContentBody>
</template>
