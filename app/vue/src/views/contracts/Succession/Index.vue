<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useRoute, useRouter } from 'vue-router'
import { Succession } from '@/store/types/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContNavigation from '@/views/contracts/Register/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Register/components/ContractorAlert.vue'
import ContController from './components/ContController.vue'
import SuccessionButton from './components/SuccessionButton.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import SuccessionList from './components/SuccessionList.vue'
// import SuccessionForm from './components/SuccessionForm.vue'

const page = ref(1)

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const downloadUrl = computed(
  () => `/excel/succession/?project=${project.value}`,
)

const contractStore = useContract()
const contractor = computed(() => contractStore.contractor)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)
const fetchContractor = (contor: number) =>
  contractStore.fetchContractor(contor)
const fetchContractorList = (projId: number, search?: string) =>
  contractStore.fetchContractorList(projId, search)

const fetchSuccession = (pk: number) => contractStore.fetchSuccession(pk)
const fetchSuccessionList = (projId: number, page?: number) =>
  contractStore.fetchSuccessionList(projId, page)

const createSuccession = (payload: Succession & { project: number }) =>
  contractStore.createSuccession(payload)
const updateSuccession = (
  payload: Succession & { project: number; page: number },
) => contractStore.updateSuccession(payload)

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
})

const router = useRouter()

const onSelectAdd = (target: number) => {
  if (!!target) fetchSuccessionList(target)
  else {
    contractStore.contract = null
    contractStore.contractor = null
    contractStore.contractorList = []
    contractStore.successionList = []
  }
  router.push({ name: '권리 의무 승계' })
}

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

const onSubmit = (payload: Succession) => {
  const projId = project.value || initProjId.value
  if (!payload.pk) createSuccession({ project: projId, ...payload })
  else updateSuccession({ page: page.value, project: projId, ...payload })
}

onBeforeMount(() => {
  if (route.query.contractor) fetchContractor(Number(route.query.contractor))
  else contractStore.contractor = null
  fetchSuccessionList(project.value || initProjId.value)
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
      <ContractorAlert v-if="contractor" :contractor="contractor" />
      <SuccessionButton
        v-if="contractor"
        :contractor="contractor"
        @on-submit="onSubmit"
      />
      <TableTitleRow
        title="승계 진행 건 목록"
        excel
        :url="downloadUrl"
        :disabled="!project || project"
      />
      <SuccessionList />
    </CCardBody>
    <!--    <SuccessionForm-->
    <!--      :project="project"-->
    <!--      :contract="contract"-->
    <!--      :contractor="contractor"-->
    <!--      @search-contractor="searchContractor"-->
    <!--    />-->
  </ContentBody>
</template>
