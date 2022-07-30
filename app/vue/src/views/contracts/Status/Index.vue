<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContSummary from '@/views/contracts/Status/components/ContSummary.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ContractBoard from '@/views/contracts/Status/components/ContractBoard.vue'

const store = useStore()

const project = computed(() => store.state.project.project)
const initProjId = computed(() => store.getters['accounts/initProjId'])
const excelUrl = computed(() =>
  project.value ? `excel/status/?project=${project.value.pk}` : '',
)

const fetchTypeList = (id: number) =>
  store.dispatch('project/fetchTypeList', id)
const fetchBuildingList = (id: number) =>
  store.dispatch('project/fetchBuildingList', id)
const fetchHouseUnitList = (project: { project: number }) =>
  store.dispatch('project/fetchHouseUnitList', project)

const projectUpdate = (payload: any) =>
  store.commit('project/updateState', payload)

onMounted(() => {
  fetchTypeList(initProjId.value)
  fetchBuildingList(initProjId.value)
  fetchHouseUnitList({ project: initProjId.value })
})

const onSelectAdd = (target: any) => {
  if (target !== '') {
    fetchTypeList(target)
    fetchBuildingList(target)
    fetchHouseUnitList({ project: target })
  } else {
    projectUpdate({
      unitTypeList: [],
      buildingList: [],
      houseUnitList: [],
    })
  }
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ContSummary />
      <TableTitleRow v-if="project" excel :url="excelUrl" />
      <v-divider color="grey" class="my-0" />
      <ContractBoard />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
