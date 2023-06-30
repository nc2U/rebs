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

watch(project, val => {
  contForm.value.formReset()
  if (!!val) {
    contractStore.contract = null
    contractStore.contractor = null
    dataSet(val)
  } else dataReset()
})

const getContract = (contor: string) =>
  fetchContractor(Number(contor), project.value).then(res =>
    fetchContract(res.contract),
  )

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

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

const dataSet = (pk: number) => {
  fetchOrderGroupList(pk)
  fetchKeyUnitList({ project: pk })
  fetchHouseUnitList({ project: pk })
  fetchTypeList(pk)
  fetchPayOrderList(pk)
  fetchAllProBankAccList(pk)
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

onBeforeMount(() => {
  const projectPk = project.value || projStore.initProjId
  fetchOrderGroupList(projectPk)
  fetchTypeList(projectPk)
  fetchAllProBankAccList(projectPk)
  fetchPayOrderList(projectPk)
  fetchKeyUnitList({ project: projectPk })
  fetchHouseUnitList({ project: projectPk })

  if (route.query.contractor) getContract(route.query.contractor as string)
  else {
    contractStore.contract = null
    contractStore.contractor = null
  }
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

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
