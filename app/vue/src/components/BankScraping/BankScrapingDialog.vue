<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRawTransaction } from '@/store/pinia/rawTransaction'
import { useProLedger } from '@/store/pinia/proLedger'
import { useComLedger } from '@/store/pinia/comLedger'
import type { RawBankTransaction } from '@/store/types/rawTransaction'
import BankRegisterDialog from './BankRegisterDialog.vue'

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    mode?: 'company' | 'project'
    companyId?: number | null
    projectId?: number | null
    isImprest?: boolean | null
  }>(),
  {
    mode: 'project',
    companyId: null,
    projectId: null,
    isImprest: null,
  },
)

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'confirmed'): void
}>()

const rawStore = useRawTransaction()
const proLedgerStore = useProLedger()
const comLedgerStore = useComLedger()

const isBankRegisterOpen = ref<boolean>(false)
const selectedCredential = ref<number | null>(null)

const selectedStatus = ref<string>('ready')
const imprestFilter = ref<'all' | 'trust' | 'imprest'>(
  props.isImprest === true ? 'imprest' : props.isImprest === false ? 'trust' : 'all',
)
const selectedAccounts = ref<Record<number, number | null>>({})
const isSyncingAll = ref<boolean>(false)
const isSyncingSingle = ref<boolean>(false)
const isConfirming = ref<Record<number, boolean>>({})

// 계정과목 목록 (본사 / 프로젝트 모드 분기)
const availableAccounts = computed(() => {
  if (props.mode === 'company') {
    return comLedgerStore.comAccounts
      .filter(a => !a.is_cate_only)
      .map(a => ({
        value: a.value,
        title: a.label,
        direction: a.direction,
        category: a.category,
      }))
  } else {
    return proLedgerStore.proAccounts
      .filter(a => !a.is_cate_only)
      .map(a => ({
        value: a.value,
        title: a.label,
        direction: a.direction,
        category: a.category,
      }))
  }
})

// 계정과목 자동완성 검색 커스텀 필터 (계정명 + 구분(입금/출금) 통합 검색)
const customAccountFilter = (value: any, query: string, item?: any) => {
  if (!query) return true
  const q = String(query).toLowerCase().trim()
  const title = String(value || '').toLowerCase()
  const dir = String(item?.raw?.direction || '').toLowerCase()
  return title.includes(q) || dir.includes(q)
}

// 현재 모드 및 컨텍스트(회사 / 프로젝트 / 운영비)에 해당하는 계좌 목록
const filteredCredentials = computed(() => {
  return rawStore.credentialList.filter(c => {
    if (props.mode === 'company') {
      if (c.is_project) return false
      if (props.companyId && c.company_id !== props.companyId) return false
      return true
    } else {
      if (!c.is_project) return false
      if (props.projectId && c.project_id !== props.projectId) return false
      if (props.isImprest !== null) {
        if (props.isImprest && !c.is_imprest) return false
        if (!props.isImprest && c.is_imprest) return false
      } else {
        if (imprestFilter.value === 'imprest' && !c.is_imprest) return false
        if (imprestFilter.value === 'trust' && c.is_imprest) return false
      }
      return true
    }
  })
})

// 현재 표시할 거래내역 목록 (클라이언트 사이드 실시간 필터링)
const displayedTransactions = computed(() => {
  return rawStore.rawTransList.filter(tx => {
    // 1. 도메인 모드 필터
    if (props.mode === 'company') {
      if (tx.is_project) return false
      if (props.companyId && tx.company_id !== props.companyId) return false
    } else {
      if (!tx.is_project) return false
      if (props.projectId && tx.project_id !== props.projectId) return false
      if (imprestFilter.value === 'imprest' && !tx.is_imprest) return false
      if (imprestFilter.value === 'trust' && tx.is_imprest) return false
    }

    // 2. 특정 계좌 선택 필터
    if (selectedCredential.value && tx.credential !== selectedCredential.value) {
      return false
    }

    // 3. 상태 필터
    if (selectedStatus.value && tx.status !== selectedStatus.value) {
      return false
    }

    return true
  })
})

// 고신뢰도(90% 이상) 대기 건수
const highConfidenceCount = computed(
  () =>
    displayedTransactions.value.filter(t => t.status === 'ready' && t.confidence_score >= 90)
      .length,
)

const loadData = async () => {
  // 계정과목 및 연동 계좌 로드
  if (props.mode === 'company') {
    if (comLedgerStore.comAccountList.length === 0) {
      await comLedgerStore.fetchCompanyAccounts()
    }
  } else {
    if (proLedgerStore.proAccounts.length === 0) {
      await proLedgerStore.fetchProjectAccounts()
    }
  }

  await rawStore.fetchCredentialList()
  await fetchTransactions()
}

const fetchTransactions = async () => {
  const filterParams: Record<string, any> = {
    status: selectedStatus.value || undefined,
  }

  if (props.mode === 'company') {
    if (props.companyId) filterParams.company = props.companyId
  } else {
    if (props.projectId) filterParams.project = props.projectId
    if (imprestFilter.value === 'imprest') filterParams.is_imprest = true
    if (imprestFilter.value === 'trust') filterParams.is_imprest = false
  }

  if (selectedCredential.value) {
    filterParams.credential = selectedCredential.value
  }

  await rawStore.fetchRawTransList(filterParams)

  // 추천 계정을 로컬 폼 상태로 기본 바인딩
  rawStore.rawTransList.forEach(t => {
    if (props.mode === 'company' && t.suggested_company_account) {
      selectedAccounts.value[t.pk] = t.suggested_company_account
    } else if (props.mode === 'project' && t.suggested_project_account) {
      selectedAccounts.value[t.pk] = t.suggested_project_account
    }
  })
}

// 계좌, 상태, 전도금 필터 변경 시 재조회
watch([selectedCredential, selectedStatus, imprestFilter], () => {
  fetchTransactions()
})

// 회사나 프로젝트 변경 시 자동 리로드
watch(
  () => [props.companyId, props.projectId],
  () => {
    selectedCredential.value = null
    fetchTransactions()
  },
)

watch(
  () => props.modelValue,
  val => {
    if (val) loadData()
  },
)

// 도메인 해당 계좌 일괄 동기화 (관련 계좌만 타겟팅하여 API 호출 비용 최적화)
const handleSyncAll = async () => {
  isSyncingAll.value = true
  try {
    const targetCredIds = filteredCredentials.value.map(c => c.pk)
    await rawStore.syncAllCredentials(undefined, undefined, targetCredIds)
    await fetchTransactions()
  } finally {
    isSyncingAll.value = false
  }
}

// 현재 선택 계좌 단건 수집
const handleSyncSingle = async () => {
  if (!selectedCredential.value) return
  isSyncingSingle.value = true
  try {
    await rawStore.syncCredential(selectedCredential.value)
    await fetchTransactions()
  } finally {
    isSyncingSingle.value = false
  }
}

// 단건 승인
const handleConfirm = async (tx: RawBankTransaction) => {
  isConfirming.value[tx.pk] = true
  try {
    const customAccount =
      selectedAccounts.value[tx.pk] ||
      (props.mode === 'company' ? tx.suggested_company_account : tx.suggested_project_account)
    const customContract = props.mode === 'project' ? tx.suggested_contract : null

    await rawStore.confirmRawTransaction(tx.pk, customAccount, customContract)
    await fetchTransactions()
    emit('confirmed')
  } finally {
    isConfirming.value[tx.pk] = false
  }
}

// 90% 이상 고신뢰도 일괄 승인
const handleBulkConfirm = async () => {
  if (highConfidenceCount.value === 0) return
  if (!confirm(`신뢰도 90% 이상인 ${highConfidenceCount.value}건의 거래를 일괄 승인하시겠습니까?`))
    return

  try {
    await rawStore.bulkConfirm(90)
    await fetchTransactions()
    emit('confirmed')
  } catch (e) {
    // handled by store
  }
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'success'
  if (score >= 70) return 'warning'
  return 'error'
}

onMounted(() => {
  if (props.modelValue) loadData()
})
</script>

<template>
  <v-dialog
    :model-value="props.modelValue"
    max-width="1350"
    scrollable
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card class="pa-2 bg-more-white text-body">
      <!-- 헤더 -->
      <v-card-title class="d-flex align-center justify-space-between pb-2 border-b">
        <div class="d-flex align-center">
          <v-icon color="primary" class="mr-2">mdi-bank-transfer-in</v-icon>
          <span class="text-h6 font-weight-bold">
            은행 거래내역 자동 수집 & AI 회계 분류 검토
            <v-chip
              size="small"
              :color="mode === 'company' ? 'info' : props.isImprest ? 'teal' : 'primary'"
              class="ml-2 font-weight-bold"
            >
              {{
                mode === 'company'
                  ? '본사 회계 관리'
                  : props.isImprest
                    ? '운영비(전도금) 관리'
                    : '프로젝트 출납/원장'
              }}
            </v-chip>
          </span>
        </div>
        <div class="d-flex align-center ga-2">
          <v-btn
            color="primary"
            variant="tonal"
            size="small"
            prepend-icon="mdi-shield-key-outline"
            @click="isBankRegisterOpen = true"
          >
            + 새 계좌/인증서 연동
          </v-btn>
          <v-btn
            icon="mdi-close"
            variant="text"
            size="small"
            @click="emit('update:modelValue', false)"
          />
        </div>
      </v-card-title>

      <!-- 툴바 컨트롤러 -->
      <v-card-text class="pt-4 pb-2">
        <v-row dense align="center">
          <!-- 연동 계좌 선택 -->
          <v-col cols="12" sm="4" md="3">
            <v-select
              v-model="selectedCredential"
              :items="[{ pk: null, account_alias: '전체 계좌 보기' }, ...filteredCredentials]"
              item-title="account_alias"
              item-value="pk"
              label="연동 계좌 선택"
              density="compact"
              variant="outlined"
              hide-details
            >
              <template #item="{ props: itemProps, item }">
                <v-list-item
                  v-bind="itemProps"
                  :subtitle="
                    (item as any)?.raw?.pk
                      ? `${(item as any)?.raw?.bank_code || ''} | ${(item as any)?.raw?.account_number || ''}`
                      : '모든 연동 계좌의 거래내역 표시'
                  "
                >
                  <template #append v-if="(item as any)?.raw?.is_imprest">
                    <v-chip size="x-small" color="teal" variant="flat">운영비 전도금</v-chip>
                  </template>
                </v-list-item>
              </template>
            </v-select>
          </v-col>

          <!-- 프로젝트 모드일 때: 계좌 성격 필터 (신탁수납 vs 운영비전도금) - isImprest prop이 고정되지 않은 경우에만 표시 -->
          <v-col v-if="mode === 'project' && isImprest === null" cols="12" sm="3" md="2">
            <v-select
              v-model="imprestFilter"
              :items="[
                { title: '전체 (수납+운영비)', value: 'all' },
                { title: '신탁/수납 전용', value: 'trust' },
                { title: '운영비 전도금', value: 'imprest' },
              ]"
              density="compact"
              variant="outlined"
              hide-details
              label="계좌 유형"
            />
          </v-col>

          <!-- 처리 상태 필터 -->
          <v-col cols="12" sm="3" md="2">
            <v-select
              v-model="selectedStatus"
              :items="[
                { title: '컨펌 대기 (Ready)', value: 'ready' },
                { title: 'AI 분류 대기 (Pending)', value: 'pending' },
                { title: '승인 완료 (Confirmed)', value: 'confirmed' },
                { title: '전체 상태 보기', value: '' },
              ]"
              density="compact"
              variant="outlined"
              hide-details
              label="처리 상태"
            />
          </v-col>

          <!-- 액션 버튼 영역 -->
          <v-col
            cols="12"
            :sm="mode === 'project' ? 12 : 5"
            :md="mode === 'project' ? 5 : 5"
            class="d-flex justify-end ga-2"
          >
            <!-- 1회 전사 통합 수집 -->
            <v-btn
              color="primary"
              variant="flat"
              size="large"
              density="compact"
              prepend-icon="mdi-sync"
              :loading="isSyncingAll"
              title="시스템에 등록된 모든 은행 계좌의 최신 거래를 1회에 일괄 수집합니다"
              @click="handleSyncAll"
            >
              전체 일괄 수집
            </v-btn>

            <!-- 선택 계좌 단건 수집 -->
            <v-btn
              v-if="selectedCredential"
              color="primary"
              variant="outlined"
              size="large"
              density="compact"
              prepend-icon="mdi-bank-sync"
              :loading="isSyncingSingle"
              @click="handleSyncSingle"
            >
              선택계좌 수집
            </v-btn>

            <!-- 고신뢰도 일괄 승인 -->
            <v-btn
              color="success"
              variant="elevated"
              size="large"
              density="compact"
              prepend-icon="mdi-check-all"
              :disabled="highConfidenceCount === 0"
              @click="handleBulkConfirm"
            >
              고신뢰도 일괄 승인 ({{ highConfidenceCount }}건)
            </v-btn>
          </v-col>
        </v-row>

        <!-- 메인 데이터 테이블 -->
        <v-table density="compact" hover class="border mt-3">
          <thead class="bg-grey-lighten-4">
            <tr>
              <th class="text-center" style="width: 100px">거래일시</th>
              <th class="text-center" style="width: 70px">구분</th>
              <th class="text-right" style="width: 110px">금액</th>
              <th class="text-left" style="width: 180px">거래처 / 적요</th>
              <th class="text-left" style="width: 230px">
                {{ mode === 'company' ? '본사 추천 계정과목' : '프로젝트 추천 계정과목' }}
              </th>
              <th v-if="mode === 'project'" class="text-left" style="width: 170px">
                추천 분양계약
              </th>
              <th class="text-left">AI 신뢰도 & 추천 사유</th>
              <th class="text-center" style="width: 90px">승인</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="rawStore.isLoading">
              <td :colspan="mode === 'project' ? 8 : 7" class="text-center py-6 text-grey">
                <v-progress-circular indeterminate color="primary" size="24" class="mr-2" />
                거래내역을 불러오는 중입니다...
              </td>
            </tr>
            <tr v-else-if="displayedTransactions.length === 0">
              <td :colspan="mode === 'project' ? 8 : 7" class="text-center py-6 text-grey">
                조회된 거래내역이 없습니다. (상단의 [전체 일괄 수집] 버튼을 눌러 은행 거래를
                가져오세요)
              </td>
            </tr>
            <tr
              v-for="tx in displayedTransactions"
              :key="tx.pk"
              :class="{ 'bg-grey-lighten-5': tx.status === 'confirmed' }"
            >
              <!-- 일시 -->
              <td class="text-center text-caption font-weight-medium">
                <div>{{ tx.deal_date }}</div>
                <div class="text-grey text-caption" style="font-size: 11px">
                  {{ tx.deal_time || '' }}
                </div>
              </td>

              <!-- 구분 -->
              <td class="text-center">
                <v-chip
                  :color="tx.sort_type === 'deposit' ? 'primary' : 'error'"
                  size="x-small"
                  variant="tonal"
                  class="font-weight-bold"
                >
                  {{ tx.sort_type === 'deposit' ? '입금' : '출금' }}
                </v-chip>
              </td>

              <!-- 금액 -->
              <td
                class="text-right font-weight-bold"
                :class="tx.sort_type === 'deposit' ? 'text-primary' : 'text-error'"
              >
                {{ (tx.amount || 0).toLocaleString() }}원
              </td>

              <!-- 거래처 / 적요 -->
              <td class="text-left">
                <div
                  class="font-weight-bold text-truncate"
                  style="max-width: 170px"
                  :title="tx.client_name"
                >
                  {{ tx.client_name || '-' }}
                </div>
                <div
                  class="text-caption text-grey text-truncate"
                  style="max-width: 170px"
                  :title="tx.content"
                >
                  {{ tx.content || '-' }}
                </div>
              </td>

              <!-- 추천 계정과목 (선택 가능 드롭다운) -->
              <td class="text-left">
                <v-autocomplete
                  v-if="tx.status !== 'confirmed'"
                  v-model="selectedAccounts[tx.pk]"
                  :items="availableAccounts"
                  density="compact"
                  variant="underlined"
                  hide-details
                  style="min-width: 190px"
                  item-value="value"
                  item-title="title"
                  clearable
                  placeholder="계정 검색/선택"
                  no-data-text="일치하는 계정과목이 없습니다"
                  :custom-filter="customAccountFilter"
                  auto-select-first
                >
                  <template #item="{ props: itemProps, item }">
                    <v-list-item
                      v-bind="itemProps"
                      :subtitle="
                        (item as any)?.raw?.direction
                          ? `[${(item as any)?.raw?.direction}]`
                          : undefined
                      "
                    />
                  </template>
                </v-autocomplete>

                <span v-else class="text-caption font-weight-medium text-success">
                  {{
                    mode === 'company'
                      ? tx.suggested_company_account_name
                      : tx.suggested_project_account_name || '반영 완료'
                  }}
                </span>
              </td>

              <!-- 추천 분양계약 (프로젝트 모드일 때만 표시) -->
              <td v-if="mode === 'project'" class="text-left">
                <div v-if="tx.suggested_contract_name" class="d-flex align-center">
                  <v-icon size="small" color="success" class="mr-1">mdi-home-check</v-icon>
                  <span
                    class="text-caption font-weight-bold text-truncate"
                    style="max-width: 140px"
                  >
                    {{ tx.suggested_contract_name }}
                  </span>
                </div>
                <span v-else class="text-caption text-grey">-</span>
              </td>

              <!-- AI 신뢰도 & 추천 사유 -->
              <td class="text-left">
                <div class="d-flex align-center">
                  <v-chip
                    :color="getScoreColor(tx.confidence_score)"
                    size="x-small"
                    variant="flat"
                    class="font-weight-bold mr-2"
                  >
                    {{ tx.confidence_score }}%
                  </v-chip>
                  <span
                    class="text-caption text-truncate"
                    style="max-width: 250px"
                    :title="tx.ai_reason"
                  >
                    {{ tx.ai_reason || '-' }}
                  </span>
                </div>
              </td>

              <!-- 승인 버튼 -->
              <td class="text-center">
                <v-btn
                  v-if="tx.status !== 'confirmed'"
                  size="x-small"
                  color="primary"
                  variant="flat"
                  :loading="isConfirming[tx.pk]"
                  @click="handleConfirm(tx)"
                >
                  승인
                </v-btn>
                <v-chip v-else size="x-small" color="grey" variant="tonal"> 완료 </v-chip>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>

      <!-- 푸터 -->
      <v-card-actions class="d-flex justify-space-between px-4 py-2 border-t bg-more-light">
        <div class="text-caption text-grey-darken-1">
          * 은행 API 수집 거래는 임시 버퍼에 안전하게 보관되며, [승인] 시 정식 출납 장부로
          반영됩니다.
        </div>
        <v-btn variant="flat" color="light" size="small" @click="emit('update:modelValue', false)">
          닫기
        </v-btn>
      </v-card-actions>
    </v-card>

    <BankRegisterDialog
      v-model="isBankRegisterOpen"
      :company-id="props.companyId"
      :project-id="props.projectId"
      @registered="loadData"
    />
  </v-dialog>
</template>
