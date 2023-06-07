<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin2'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContNavigation from '@/views/contracts/Register/components/ContNavigation.vue'
import ContController from './components/ContController.vue'
import ContractorAlert from './components/ContractorAlert.vue'
import SuccessionForm from './components/SuccessionForm.vue'

const projectStore = useProject()
const project = computed(() => projectStore.project?.pk)

const contractStore = useContract()
const contract = computed(() => contractStore.contract)
const contractor = computed(() => contractStore.contractor)

const fetchContract = (cont: number) => contractStore.fetchContract(cont)
const fetchContractor = (contor: number) =>
  contractStore.fetchContractor(contor)
const fetchContractorList = (projId: number, search?: string) =>
  contractStore.fetchContractorList(projId, search)

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
  else console.log('nop!')
})

const router = useRouter()

const onSelectAdd = (target: number) => {
  if (!target) {
    contractStore.contract = null
    contractStore.contractor = null
    contractStore.contractorList = []
  }
  router.push({ name: '권리 의무 승계' })
}

const searchContractor = (search: string) => {
  if (search !== '' && project.value) {
    fetchContractorList(project.value, search)
  } else contractStore.contractorList = []
}

onBeforeMount(() => {
  if (route.query.contractor) fetchContractor(Number(route.query.contractor))
  else contractStore.contractor = null
})

onBeforeRouteLeave(() => {
  contractStore.contract = null
  contractStore.contractor = null
  contractStore.contRelease = null
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
      <SuccessionForm :contract="contract" :contractor="contractor" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
