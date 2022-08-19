<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useStore } from 'vuex'
import { useProject } from '@/store/pinia/project'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ReleasetButton from '@/views/contracts/Release/components/ReleasetButton.vue'
import ContNavigation from '@/views/contracts/Release/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Release/components/ContractorAlert.vue'
import ContController from '@/views/contracts/Release/components/ContController.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ReleaseList from '@/views/contracts/Release/components/ReleaseList.vue'

const page = ref(1)

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)
const initProjId = computed(() => projectStore.initProjId)
const downloadUrl = computed(() => `/excel/releases/?project=${project.value}`)

const store = useStore()
const contractor = computed(() => store.state.contract.contractor)

const fetchContractor = (contor: any) =>
  store.dispatch('contract/fetchContractor', contor)
const fetchContractorList = (payload: any) =>
  store.dispatch('contract/fetchContractorList', payload)
const fetchContRelease = (payload: any) =>
  store.dispatch('contract/fetchContRelease', payload)
const fetchContReleaseList = (payload: { project: number } & any) =>
  store.dispatch('contract/fetchContReleaseList', payload)
const createRelease = (payload: any) =>
  store.dispatch('contract/createRelease', payload)
const updateRelease = (payload: any) =>
  store.dispatch('contract/updateRelease', payload)

const route = useRoute()

watch(route, val => {
  if (val.query.contractor) fetchContractor(val.query.contractor)
  else store.commit('contract/updateState', { contractor: null })
})

watch(contractor, val => {
  if (val && val.contractorrelease) fetchContRelease(val.contractorrelease)
})

const router = useRouter()

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchContReleaseList({ project: target })
  } else {
    store.commit('contract/updateState', {
      contractor: null,
      contractorList: [],
      contRelease: null,
      contReleaseList: [],
      contReleaseCount: 0,
    })
  }
  router.push({ name: '계약해지 관리' })
}
const searchContractor = (search: string) => {
  if (search !== '') {
    fetchContractorList({ project: project.value, search })
  } else store.commit('contract/updateState', { contractorList: [] })
}

const getRelease = (release: number) => fetchContRelease(release)

const pageSelect = (p: number) => {
  page.value = p
  fetchContReleaseList({ project: project.value, page: p })
}

const onSubmit = (payload: any) => {
  if (payload.pk)
    updateRelease({ project: project.value, page: page.value, ...payload })
  else createRelease({ project: project.value, ...payload })
}

onBeforeMount(() => {
  fetchContReleaseList({ project: initProjId.value })
  if (route.query.contractor) fetchContractor(route.query.contractor)
  else store.commit('contract/updateState', { contractor: null }) // this.FETCH_CONTRACTOR(null)
})

onBeforeRouteLeave(() =>
  store.commit('contract/updateState', { contractor: null }),
)
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContNavigation :contractor="contractor" />
      <ContController
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
        v-if="project"
        title="계약해지 현황"
        color="error"
        excel
        :url="downloadUrl"
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
