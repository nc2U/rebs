<script lang="ts" setup>
import { computed, onBeforeMount, watch } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractForm from '@/views/contracts/Register/components/ContractForm.vue'

const route = useRoute()
const router = useRouter()

const store = useStore()
const contract = computed(() => store.state.contract.contract)
const unitSet = computed(() => project.value?.is_unit_set)
const isUnion = computed(() => !project.value?.is_direct_manage)

const projectStore = useProject()
const project = computed(() => projectStore.project)
const initProjId = computed(
  () => contract.value?.project || projectStore.initProjId,
)

const fetchContract = (cont: any) =>
  store.dispatch('contract/fetchContract', cont)
const fetchOrderGroupList = (projId: number) =>
  store.dispatch('contract/fetchOrderGroupList', projId)
const fetchKeyUnitList = (payload: any) =>
  store.dispatch('contract/fetchKeyUnitList', payload)
const fetchHouseUnitList = (payload: any) =>
  store.dispatch('contract/fetchHouseUnitList', payload)
const createContractSet = (payload: any) =>
  store.dispatch('contract/createContractSet', payload)
const updateContractSet = (payload: any) =>
  store.dispatch('contract/updateContractSet', payload)

const fetchTypeList = (projId: number) =>
  store.dispatch('project/fetchTypeList', projId)
const fetchProBankAccList = (projId: number) =>
  store.dispatch('proCash/fetchProBankAccList', projId)
const fetchPayOrderList = (projId: number) =>
  store.dispatch('payment/fetchPayOrderList', projId)

watch(contract, newVal => {
  const projId = project.value?.pk || initProjId.value
  if (newVal) {
    fetchKeyUnitList({
      project: projId,
      unit_type: newVal.unit_type.pk,
      contract: route.query.contract,
      available: 'false',
    })
    if (newVal.keyunit.houseunit) {
      fetchHouseUnitList({
        project: projId,
        unit_type: newVal.unit_type.pk,
        contract: route.query.contract,
      })
    } else {
      fetchHouseUnitList({
        project: projId,
        unit_type: newVal.unit_type.pk,
      })
    }
  }
})

const onSelectAdd = (target: any) => {
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
const typeSelect = (type: number) => {
  const unit_type = type
  fetchKeyUnitList({ project: project.value?.pk, unit_type })
  fetchHouseUnitList({ project: project.value?.pk, unit_type })
}
const getContract = (cont: any) => fetchContract(cont)

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
      :contract="contract"
      :unit-set="unitSet"
      :is-union="isUnion"
      @type-select="typeSelect"
      @on-create="onCreate"
      @on-update="onUpdate"
    />
  </ContentBody>
</template>
