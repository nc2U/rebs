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

const projStore = useProject()
const project = computed(() => projStore.project?.pk)

const downloadUrl = computed(
  () => `/excel/successions/?project=${project.value}`,
)

const contStore = useContract()
const contractor = computed(() => contStore.contractor)

const fetchContract = (cont: number) => contStore.fetchContract(cont)
const fetchContractor = (contor: number) => contStore.fetchContractor(contor)
const fetchContractorList = (projId: number, search?: string) =>
  contStore.fetchContractorList(projId, search)

const fetchSuccession = (pk: number) => contStore.fetchSuccession(pk)
const fetchSuccessionList = (projId: number, page?: number) =>
  contStore.fetchSuccessionList(projId, page)

const fetchBuyerList = (projId: number) => contStore.fetchBuyerList(projId)

const createBuyer = (payload: Succession & Buyer & { project: number }) =>
  contStore.createBuyer(payload)

const patchSuccession = (
  payload: Succession & Buyer & { project: number; page: number },
) => contStore.patchSuccession(payload)

const route = useRoute()
watch(route, val => {
  if (val.query.contractor) fetchContractor(Number(val.query.contractor))
  else {
    contStore.contract = null
    contStore.contractor = null
  }
})

watch(contractor, val => {
  if (val) fetchContract(val.contract)
  if (val?.successions.length) fetchSuccession(val.successions[0].pk)
  else {
    contStore.contract = null
    contStore.succession = null
  }
})

watch(project, val => {
  router.replace({ name: '권리 의무 승계' })
  if (!!val) dataSet(val)
  else dataReset()
})

const router = useRouter()

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contStore.contractorList = []
}

const pageSelect = (p: number) => {
  page.value = p
  if (project.value) fetchSuccessionList(project.value, p)
}

const onSubmit = (payload: { s_data: Succession; b_data: Buyer }) => {
  const { s_data, b_data } = payload
  const dbData = { ...s_data, ...b_data }
  if (!!project.value) {
    if (!s_data.pk) {
      createBuyer({ ...dbData, project: project.value })
      router.push({ name: '권리 의무 승계' })
    } else
      patchSuccession({
        ...dbData,
        project: project.value,
        page: page.value,
      })
  } else alert('프로젝트를 선택하여 주세요!')
}

const dataSet = (pk: number) => {
  fetchSuccessionList(pk)
  fetchBuyerList(pk)
}

const dataReset = () => {
  contStore.contract = null
  contStore.contractor = null
  contStore.contractorList = []
  contStore.successionList = []
  contStore.buyerList = []
}

onBeforeMount(() => {
  if (route.query.contractor) fetchContractor(Number(route.query.contractor))
  else contStore.contractor = null
  dataSet(project.value || projStore.initProjId)
})
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContNavigation :cont-on="contractor?.status < '3'" />
      <ContController
        :project="project"
        @search-contractor="searchContractor"
      />
      <ContractorAlert v-if="contractor" :contractor="contractor" />
      <SuccessionButton v-if="contractor" @on-submit="onSubmit" />
      <TableTitleRow
        title="승계 진행 건 목록"
        excel
        :url="downloadUrl"
        :disabled="!project"
      />
      <SuccessionList @page-select="pageSelect" @on-submit="onSubmit" />
    </CCardBody>
  </ContentBody>
</template>
