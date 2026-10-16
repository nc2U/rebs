<script lang="ts" setup>
import { ref, computed, onBeforeMount, watch, nextTick } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { navMenu, pageTitle } from '@/views/contracts/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import { useContract } from '@/store/pinia/contract'
import { usePerms } from '@/composables/usePerms'
import type { Project } from '@/store/types/project'
import type { BuyerForm, Contractor, Succession } from '@/store/types/contract'
import Loading from '@/components/Loading/Index.vue'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ContractAuthGuard from '@/components/AuthGuard/ContractAuthGuard.vue'
import ContNavigation from '@/views/contracts/Manage/components/ContNavigation.vue'
import ContractorAlert from '@/views/contracts/Manage/components/ContractorAlert.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ContController from './components/ContController.vue'
import SuccessionButton from './components/SuccessionButton.vue'
import SuccessionList from './components/SuccessionList.vue'
import SuccessionForm from './components/SuccessionForm.vue'

const { can, PERM } = usePerms()
const canContractUpdate = computed(() => can(PERM.CONTRACT_UPDATE))

const route = useRoute()
const router = useRouter()
const projStore = useProject()
const contStore = useContract()

const page = ref(1)
const loading = ref(true)

const successionFormModal = ref<InstanceType<typeof FormModal> | null>(null)
const successionAlertModal = ref<InstanceType<typeof AlertModal> | null>(null)

// 쿼리/파라미터 안전 파싱 (NaN 방어)
const parseNumber = (val: unknown): number | null => {
  if (!val) return null
  const parsed = parseInt(String(val), 10)
  return Number.isNaN(parsed) ? null : parsed
}

const highlightId = computed(() => parseNumber(route.query.highlight_id))
const urlProjectId = computed(() => parseNumber(route.query.project))
const contractorId = computed(() => parseNumber(route.params.contractorId))
const project = computed<number | null>(() => (projStore.project as Project | null)?.pk ?? null)

const downloadUrl = computed(() => `/excel/successions/?project=${project.value ?? ''}`)

const contractor = computed<Contractor | null>(() => contStore.contractor)
const contOn = computed(() => !!contractor.value && contractor.value.status < '3')
const succession = computed<Succession | null>(() => contStore.succession)
const isSuccession = computed(() => !!succession.value && succession.value.status !== '3')

// 라우트 contractorId 감시
watch(
  contractorId,
  async newId => {
    if (newId) {
      await contStore.fetchContractor(newId)
    } else {
      contStore.contract = null
      contStore.contractor = null
      contStore.succession = null
    }
  },
)

// 계약자 변경 시 연관 데이터 독립 갱신 (if-else 논리 버그 해결)
watch(contractor, async val => {
  if (val?.contract) {
    await contStore.fetchContract(val.contract)
  } else {
    contStore.contract = null
  }

  if (val?.succession?.pk) {
    await contStore.fetchSuccession(val.succession.pk)
  } else {
    contStore.succession = null
  }
})

const searchContractor = async (search: string) => {
  if (search.trim() !== '' && project.value) {
    await contStore.fetchContractorList(project.value, search.trim())
  } else {
    contStore.contractorList = []
  }
}

// 임시 쿼리만 선택적으로 정리 (project 등 영구 파라미터 보존)
const clearTransientQueries = (preserveHighlight = false) => {
  if (route.query.page || route.query.highlight_id || route.query.contractor) {
    const nextQuery = { ...route.query }
    if (!preserveHighlight) delete nextQuery.highlight_id
    delete nextQuery.page
    delete nextQuery.contractor
    router.replace({ query: nextQuery }).catch(() => {})
  }
}

const pageSelect = async (p: number) => {
  clearTransientQueries(!!highlightId.value)
  page.value = p
  if (project.value) {
    await contStore.fetchSuccessionList(project.value, p)
  }
}

const scrollToHighlight = async () => {
  if (!highlightId.value) return
  await nextTick()
  setTimeout(() => {
    const element = document.querySelector(`[data-succession-id="${highlightId.value}"]`)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  }, 100)
}

const loadHighlightPage = async (projectId: number) => {
  if (!highlightId.value || !projectId) return
  try {
    const targetPage = await contStore.findSuccessionPage(highlightId.value, projectId)
    page.value = targetPage
    await contStore.fetchSuccessionList(projectId, targetPage)
  } catch (error) {
    console.error('승계 하이라이트 페이지 로드 오류:', error)
    await contStore.fetchSuccessionList(projectId, 1)
  }
}

const dataSetup = async (pk: number) => {
  if (highlightId.value) {
    await loadHighlightPage(pk)
  } else {
    await contStore.fetchSuccessionList(pk, page.value)
  }
  await scrollToHighlight()
}

const dataReset = () => {
  contStore.contract = null
  contStore.contractor = null
  contStore.contractorList = []
  contStore.successionList = []
  contStore.succession = null
}

const projSelect = async (target: number | null, isAuto = false) => {
  if (!isAuto) clearTransientQueries(false)
  dataReset()

  if (target) {
    if (isAuto) await projStore.fetchProject(target)
    await dataSetup(target)
  }
}

const callFormModal = (suc?: Succession) => {
  if (canContractUpdate.value) {
    if (suc) {
      contStore.succession = suc
    }
    successionFormModal.value?.callModal()
  } else {
    successionAlertModal.value?.callModal()
  }
}

const doneAlert = () => {
  successionAlertModal.value?.callModal(
    '',
    '승계 완료된 건 입니다. 신규 승계 건을 등록하려면 해당 계약자를 선택하십시요.',
  )
}

const onSubmit = async (payload: { s_data: Succession; b_data: BuyerForm }) => {
  const { s_data, b_data } = payload
  const dbData = { ...s_data, ...b_data }

  if (!isSuccession.value && !s_data.pk) {
    await contStore.createSuccession({ ...dbData, project: project.value as number, page: 1 })
    router.push({ name: '권리 의무 승계 보기', params: { contractorId: s_data.seller.pk } })
  } else {
    await contStore.patchSuccession({
      ...dbData,
      project: project.value as number,
      page: page.value,
    })
  }
  successionFormModal.value?.close()
}

const onDelete = async (pk: number) => {
  if (project.value) {
    await contStore.deleteSuccession(pk, project.value, page.value)
  }
  successionFormModal.value?.close()
}

// 라우트 갱신 감지 (project.value 참조 오류 해결)
onBeforeRouteUpdate(async to => {
  const toProjectId = parseNumber(to.query.project)

  if (toProjectId && toProjectId !== project.value) {
    await projSelect(toProjectId, true)
  } else if (to.query.highlight_id) {
    const currentProjId = project.value || projStore.currentProject
    if (currentProjId) await dataSetup(currentProjId)
  }
})

onBeforeMount(async () => {
  // targetId 판별 안전화 (currentProject 부재 시에도 urlProjectId 지원)
  const targetId = urlProjectId.value || project.value || projStore.currentProject

  if (targetId) {
    if (urlProjectId.value && urlProjectId.value !== project.value) {
      await projSelect(urlProjectId.value, true)
    } else {
      if (contractorId.value) {
        await contStore.fetchContractor(contractorId.value)
      } else {
        contStore.contractor = null
      }
      await dataSetup(targetId)
    }
  }

  loading.value = false
})
</script>

<template>
  <ContractAuthGuard>
    <Loading v-model:active="loading" />
    <ContentHeader
      :page-title="pageTitle"
      :nav-menu="navMenu"
      selector="ProjectSelect"
      @proj-select="projSelect($event, false)"
    />

    <ContentBody>
      <CCardBody class="pb-5">
        <ContNavigation :cont-on="!!contOn" :contractor="contractor?.pk" />
        <ContController :project="project ?? undefined" @search-contractor="searchContractor" />
        <ContractorAlert v-if="contractor" :contractor="contractor" clear-route="권리 의무 승계" />

        <SuccessionButton
          v-if="canContractUpdate && contractor"
          :is-succession="isSuccession"
          @call-form="callFormModal"
        />
        <TableTitleRow
          title="승계 진행 건 목록"
          excel
          :url="downloadUrl"
          filename="승계_진행건_목록.xlsx"
          :disabled="!project"
        />
        <SuccessionList
          :highlight-id="highlightId ?? undefined"
          :current-page="page"
          @page-select="pageSelect"
          @call-form="callFormModal"
          @done-alert="doneAlert"
        />
      </CCardBody>
    </ContentBody>

    <FormModal ref="successionFormModal" size="lg">
      <template #header>권리 의무 승계 수정 등록</template>
      <template #default>
        <SuccessionForm
          :succession="succession ?? undefined"
          :is-succession="isSuccession"
          @on-submit="onSubmit"
          @on-delete="onDelete"
          @close="successionFormModal?.close()"
        />
      </template>
    </FormModal>

    <AlertModal ref="successionAlertModal" />
  </ContractAuthGuard>
</template>
