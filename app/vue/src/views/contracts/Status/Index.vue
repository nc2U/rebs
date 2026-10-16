<script lang="ts" setup>
import { ref, computed, onBeforeMount, provide } from 'vue'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'
import { pageTitle, navMenu } from '@/views/contracts/_menu/headermixin'
import type { Project } from '@/store/types/project'
import { useProject } from '@/store/pinia/project'
import { useProjectData } from '@/store/pinia/project_data'
import { useContract } from '@/store/pinia/contract'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractAuthGuard from '@/components/AuthGuard/ContractAuthGuard.vue'
import Loading from '@/components/Loading/Index.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ContSummary from './components/ContSummary.vue'
import ContractBoard from './components/ContractBoard.vue'

const route = useRoute()
const projStore = useProject()
const pDataStore = useProjectData()
const contStore = useContract()

const isContor = ref<boolean>(true)
const isPageLoading = ref<boolean>(false)

// 계약자명 표시 상태 주입 (하위 컴포넌트 호환)
provide('isContor', isContor)

// 쿼리 파라미터 안전 파싱
const parseQueryNumber = (val: unknown): number | null => {
  if (!val) return null
  const parsed = parseInt(String(val), 10)
  return Number.isNaN(parsed) ? null : parsed
}

const urlProjectId = computed(() => parseQueryNumber(route.query.project))
const project = computed<number | null>(() => (projStore.project as Project)?.pk ?? null)

const excelUrl = computed(() =>
  project.value ? `/excel/status/?project=${project.value}&iscontor=${isContor.value}` : '',
)

// 프로젝트 데이터 세팅 (불필요한 fetchContractList 제거 및 병렬 처리)
const dataSetup = async (pk: number) => {
  isPageLoading.value = true
  try {
    await Promise.all([
      pDataStore.fetchTypeList(pk),
      pDataStore.fetchBuildingList(pk),
      pDataStore.fetchHouseUnitList(pk),
      contStore.fetchSubsSummaryList(pk),
      contStore.fetchContSummaryList(pk),
    ])
  } catch (error) {
    console.error('동호수 현황 데이터를 불러오는 중 오류가 발생했습니다:', error)
  } finally {
    isPageLoading.value = false
  }
}

const dataReset = () => {
  pDataStore.$patch({
    unitTypeList: [],
    buildingList: [],
    houseUnitList: [],
  })
  contStore.$patch({
    subsSummaryList: [],
    contSummaryList: [],
    contractsCount: 0,
  })
}

const projSelect = async (target: number | null, isAuto = false) => {
  dataReset()
  if (target) {
    if (isAuto) await projStore.fetchProject(target)
    await dataSetup(target)
  }
}

// 라우트 쿼리 변경 감지
onBeforeRouteUpdate(async to => {
  const toProjectId = parseQueryNumber(to.query.project)
  if (toProjectId && toProjectId !== project.value) {
    await projSelect(toProjectId, true)
  }
})

onBeforeMount(async () => {
  const targetId = urlProjectId.value || project.value || projStore.currentProject
  if (targetId) {
    if (urlProjectId.value && urlProjectId.value !== project.value) {
      await projSelect(urlProjectId.value, true)
    } else {
      await dataSetup(targetId)
    }
  }
})
</script>

<template>
  <ContractAuthGuard>
    <Loading v-model:active="isPageLoading" />
    <ContentHeader
      :page-title="pageTitle"
      :nav-menu="navMenu"
      selector="ProjectSelect"
      @proj-select="projSelect($event, false)"
    />

    <ContentBody>
      <CCardBody class="pb-5">
        <ContSummary />
        <TableTitleRow excel :url="excelUrl" filename="동호수현황표.xlsx" :disabled="!project">
          <div class="p-2">
            <CFormSwitch
              id="flexCheckDefault"
              v-model="isContor"
              label="계약자명 표시"
              style="font-size: 0.825em"
              :disabled="!project"
            />
          </div>
        </TableTitleRow>
        <v-divider color="grey" class="my-0" />
        <ContractBoard />
      </CCardBody>
    </ContentBody>
  </ContractAuthGuard>
</template>
