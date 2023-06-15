<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { ContractRelease } from '@/store/types/contract'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ReleasetButton from '@/views/contracts/Release/components/ReleasetButton.vue'
import ContNavigation from '@/views/contracts/Register/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Release/components/ContractorAlert.vue'
import ContController from '@/views/contracts/Release/components/ContController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ReleaseList from '@/views/contracts/Release/components/ReleaseList.vue'

const page = ref(1)

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)

const downloadUrl = computed(() => `/excel/releases/?project=${project.value}`)

const contractStore = useContract()
const contractor = computed(() => contractStore.contractor)
const contOn = computed(() => contractor.value && contractor.value.status < '3')

const fetchContractor = (contor: number) =>
  contractStore.fetchContractor(contor)

const fetchContractorList = (projId: number, search?: string) =>
  contractStore.fetchContractorList(projId, search)
const fetchContRelease = (pk: number) => contractStore.fetchContRelease(pk)
const fetchContReleaseList = (projId: number, page?: number) =>
  contractStore.fetchContReleaseList(projId, page)

const createRelease = (payload: ContractRelease) =>
  contractStore.createRelease(payload)
const updateRelease = (payload: ContractRelease & { page: number }) =>
  contractStore.updateRelease(payload)

const route = useRoute()
watch(route, val => {
  if (val.query.contractor) {
    fetchContractor(Number(val.query.contractor))
  } else contractStore.contractor = null
})

watch(contractor, val => {
  if (val?.contractorrelease) fetchContRelease(val.contractorrelease)
  else contractStore.contRelease = null
})

const router = useRouter()

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchContReleaseList(target)
  } else {
    contractStore.contractor = null
    contractStore.contractorList = []
    contractStore.contRelease = null
    contractStore.contReleaseList = []
    contractStore.contReleaseCount = 0
  }
  router.push({ name: '계약 해지 관리' })
}
const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

const getRelease = (release: number) => fetchContRelease(release)

const pageSelect = (p: number) => {
  page.value = p
  if (project.value) fetchContReleaseList(project.value, p)
}

const onSubmit = (payload: ContractRelease) => {
  if (project.value) payload.project = project.value
  if (!payload.pk) createRelease({ ...payload })
  else updateRelease({ page: page.value, ...payload })
}

onBeforeMount(() => {
  fetchContReleaseList(project.value || initProjId.value)
  if (route.query.contractor) fetchContractor(Number(route.query.contractor))
  else contractStore.contractor = null
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
      <ContNavigation :cont-on="contOn" />
      <ContController
        :project="project"
        @search-contractor="searchContractor"
        @get-release="getRelease"
      />
      <ContractorAlert v-if="contractor" :contractor="contractor" />
      <ReleasetButton
        v-if="contractor"
        :contractor="contractor"
        @on-submit="onSubmit"
      />
      <TableTitleRow
        title="계약 해지 현황"
        color="grey"
        excel
        :url="downloadUrl"
        :disabled="!project"
      />
      <ReleaseList
        @page-select="pageSelect"
        @get-release="getRelease"
        @on-submit="onSubmit"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
