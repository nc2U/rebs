<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { navMenu, pageTitle } from '@/views/contracts/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useRoute, useRouter } from 'vue-router'
import { Buyer, Succession } from '@/store/types/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContNavigation from '@/views/contracts/Register/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Register/components/ContractorAlert.vue'
import ContController from './components/ContController.vue'
import SuccessionButton from './components/SuccessionButton.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SuccessionList from './components/SuccessionList.vue'

const page = ref(1)

const projectStore = useProject()
const project = computed(
  () => projectStore.project?.pk || projectStore.initProjId,
)

const downloadUrl = computed(
  () => `/excel/succession/?project=${project.value}`,
)

const contractStore = useContract()
const contractor = computed(() => contractStore.contractor)

const isSuccession = computed(
  () =>
    !!contractor.value?.successions &&
    !contractor.value?.successions[0].is_approval,
)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)
const fetchContractor = (contor: number) =>
  contractStore.fetchContractor(contor)
const fetchContractorList = (projId: number, search?: string) =>
  contractStore.fetchContractorList(projId, search)

const fetchSuccession = (pk: number) => contractStore.fetchSuccession(pk)
const fetchSuccessionList = (projId: number, page?: number) =>
  contractStore.fetchSuccessionList(projId, page)

const fetchBuyerList = (projId: number) => contractStore.fetchBuyerList(projId)

const createBuyer = (payload: Succession & Buyer & { project: number }) =>
  contractStore.createBuyer(payload)

const patchSuccession = (
  payload: Succession & Buyer & { project: number; page: number },
) => contractStore.patchSuccession(payload)

const route = useRoute()
watch(route, val => {
  if (val.query.contractor) fetchContractor(Number(val.query.contractor))
  else {
    contractStore.contract = null
    contractStore.contractor = null
  }
})

watch(contractor, val => {
  if (val) fetchContract(val.contract)
  if (val?.successions) fetchSuccession(val.successions[0].pk)
  else {
    contractStore.contract = null
    contractStore.succession = null
  }
})

const router = useRouter()

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchSuccessionList(target)
    fetchBuyerList(target)
  } else {
    contractStore.contract = null
    contractStore.contractor = null
    contractStore.contractorList = []
    contractStore.successionList = []
    contractStore.buyerList = []
  }
  router.push({ name: '권리 의무 승계' })
}

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

const onSubmit = (payload: { s_data: Succession; b_data: Buyer }) => {
  const { s_data, b_data } = payload
  const dbData = { ...s_data, ...b_data }
  if (!s_data.pk) {
    createBuyer({ ...dbData, project: project.value })
    router.push({ name: '권리 의무 승계' })
  } else
    patchSuccession({ ...dbData, project: project.value, page: page.value })
  console.log({ ...dbData })
}

onBeforeMount(() => {
  if (route.query.contractor) fetchContractor(Number(route.query.contractor))
  else contractStore.contractor = null
  fetchSuccessionList(project.value)
  fetchBuyerList(project.value)
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
      <ContNavigation :cont-on="contractor?.status < '3'" />
      <ContController
        :project="project"
        @search-contractor="searchContractor"
      />
      <ContractorAlert
        v-if="contractor"
        :contractor="contractor"
        :is-succession="isSuccession"
      />
      <SuccessionButton
        v-if="contractor"
        :is-succession="isSuccession"
        @on-submit="onSubmit"
      />
      {{ contractor }}
      <hr />
      계약자 승계 상태에 따른 구분 로직 작성 / 페이지 관련 로직 작성 / 엑셀 로직
      작성
      <hr />
      <TableTitleRow
        title="승계 진행 건 목록"
        excel
        :url="downloadUrl"
        :disabled="true"
      />
      <SuccessionList @on-submit="onSubmit" />
    </CCardBody>
  </ContentBody>
</template>
