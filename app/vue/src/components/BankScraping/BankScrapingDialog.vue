<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRawTransaction } from '@/store/pinia/rawTransaction'
import { useProLedger } from '@/store/pinia/proLedger'
import { useComLedger } from '@/store/pinia/comLedger'
import type { RawBankTransaction } from '@/store/types/rawTransaction'
import BankRegisterDialog from './BankRegisterDialog.vue'
import { message } from '@/utils/helper'

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

interface SplitEntry {
  id: number
  account_id: number | null
  amount: number
  trader: string
  contract_id?: number | null
}

const splitEntries = ref<Record<number, SplitEntry[]>>({})
const isSplitOpen = ref<Record<number, boolean>>({})

// 이체수수료 계정 PK
const transferFeePk = computed(() => {
  return props.mode === 'company'
    ? comLedgerStore.transferFeePk
    : proLedgerStore.transferFeePk
})

// 분개 분할 토글
const toggleSplit = (tx: RawBankTransaction) => {
  if (isSplitOpen.value[tx.pk]) {
    isSplitOpen.value[tx.pk] = false
  } else {
    isSplitOpen.value[tx.pk] = true
    if (!splitEntries.value[tx.pk] || splitEntries.value[tx.pk].length === 0) {
      const currentAcc =
        selectedAccounts.value[tx.pk] ||
        (props.mode === 'company'
          ? tx.suggested_company_account
          : tx.suggested_project_account) ||
        null
      splitEntries.value[tx.pk] = [
        {
          id: 1,
          account_id: currentAcc,
          amount: Number(tx.amount) || 0,
          trader: tx.client_name || '',
          contract_id: tx.suggested_contract || null,
        },
      ]
    }
  }
}

// 이체수수료 500원 원클릭 자동 분할
const quickAddTransferFee = (tx: RawBankTransaction) => {
  isSplitOpen.value[tx.pk] = true
  const totalAmount = Number(tx.amount) || 0
  const feeAmount = 500
  const mainAmount = Math.max(0, totalAmount - feeAmount)
  const traderName = tx.client_name || ''
  const currentAcc =
    selectedAccounts.value[tx.pk] ||
    (props.mode === 'company'
      ? tx.suggested_company_account
      : tx.suggested_project_account) ||
    null

  splitEntries.value[tx.pk] = [
    {
      id: 1,
      account_id: currentAcc,
      amount: mainAmount,
      trader: traderName,
      contract_id: tx.suggested_contract || null,
    },
    {
      id: 2,
      account_id: transferFeePk.value ?? null,
      amount: feeAmount,
      trader: traderName ? `[${traderName}]-이체수수료` : '이체수수료',
      contract_id: null,
    },
  ]
}

// 분개 행 추가
const addSplitRow = (tx: RawBankTransaction) => {
  if (!splitEntries.value[tx.pk]) {
    splitEntries.value[tx.pk] = []
  }
  const currentTotal = splitEntries.value[tx.pk].reduce(
    (sum, e) => sum + (Number(e.amount) || 0),
    0,
  )
  const remaining = Math.max(0, Number(tx.amount) - currentTotal)

  splitEntries.value[tx.pk].push({
    id: Date.now(),
    account_id: null,
    amount: remaining,
    trader: tx.client_name || '',
    contract_id: null,
  })
}

// 분개 행 삭제
const removeSplitRow = (tx: RawBankTransaction, index: number) => {
  if (!splitEntries.value[tx.pk]) return
  splitEntries.value[tx.pk].splice(index, 1)
  if (splitEntries.value[tx.pk].length === 0) {
    isSplitOpen.value[tx.pk] = false
  }
}

// 분개 분할 취소
const cancelSplit = (tx: RawBankTransaction) => {
  isSplitOpen.value[tx.pk] = false
  delete splitEntries.value[tx.pk]
}

// 분개 합계 및 차액 계산
const getSplitTotal = (txPk: number): number => {
  const entries = splitEntries.value[txPk]
  if (!entries) return 0
  return entries.reduce((sum, e) => sum + (Number(e.amount) || 0), 0)
}

const getSplitDiff = (tx: RawBankTransaction): number => {
  return Number(tx.amount) - getSplitTotal(tx.pk)
}

// 분할 모드 유효성 검사 (차액 0 & 계정 선택 여부)
const isSplitValid = (tx: RawBankTransaction): boolean => {
  if (!isSplitOpen.value[tx.pk]) return true
  const entries = splitEntries.value[tx.pk]
  if (!entries || entries.length === 0) return false
  if (getSplitDiff(tx) !== 0) return false
  return entries.every(e => !!e.account_id && Number(e.amount) > 0)
}
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


const bankCodeMap: Record<string, string> = {
  '0004': 'KB국민',
  '0088': '신한',
  '0020': '우리',
  '0081': '하나',
  '0003': 'IBK기업',
  '0011': 'NH농협',
  '0023': 'SC제일',
  '0027': '한국씨티',
  '0002': 'KDB산업',
  '0090': '카카오뱅크',
  '0089': '케이뱅크',
  '0092': '토스뱅크',
  '0031': 'iM뱅크(대구)',
  '0032': 'BNK부산',
  '0034': '광주',
  '0037': '전북',
  '0039': 'BNK경남',
  '0071': '우체국',
  '0007': 'Sh수협',
  '0045': '새마을금고',
  '0048': '신협',
}

const getBankName = (code: string) => {
  return bankCodeMap[code] || `은행(${code})`
}

// 연동 현황 요약 (은행별 계좌 수 및 연동 방식)
const connectedBankSummary = computed(() => {
  const map: Record<string, { bank_code: string; bank_name: string; count: number; has_cert: boolean }> = {}
  filteredCredentials.value.forEach(c => {
    if (!map[c.bank_code]) {
      map[c.bank_code] = {
        bank_code: c.bank_code,
        bank_name: getBankName(c.bank_code),
        count: 0,
        has_cert: false,
      }
    }
    map[c.bank_code].count += 1
    if (c.auth_type === 'cert') {
      map[c.bank_code].has_cert = true
    }
  })
  return Object.values(map)
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
  if (filteredCredentials.value.length === 0) {
    message(
      'warning',
      '수집 안내',
      '현재 등록된 연동 계좌가 없습니다. 상단의 [+ 새 계좌/인증서 연동] 버튼을 눌러 계좌 또는 공동인증서를 먼저 연동해 주세요.',
    )
    return
  }
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

// 단건 승인 (복수 분개 분할 지원)
const handleConfirm = async (tx: RawBankTransaction) => {
  isConfirming.value[tx.pk] = true
  try {
    let customAccount: number | null = null
    let customContract: number | null = null
    let entriesPayload:
      | Array<{
          account_id: number
          amount: number
          trader?: string
          contract_id?: number | null
        }>
      | null = null

    if (isSplitOpen.value[tx.pk] && (splitEntries.value[tx.pk]?.length ?? 0) > 0) {
      if (!isSplitValid(tx)) return
      entriesPayload = splitEntries.value[tx.pk].map(e => ({
        account_id: e.account_id!,
        amount: Number(e.amount),
        trader: e.trader || undefined,
        contract_id: e.contract_id || null,
      }))
    } else {
      customAccount =
        selectedAccounts.value[tx.pk] ||
        (props.mode === 'company' ? tx.suggested_company_account : tx.suggested_project_account) ||
        null
      customContract = props.mode === 'project' ? tx.suggested_contract || null : null
    }

    await rawStore.confirmRawTransaction(tx.pk, customAccount, customContract, entriesPayload)
    isSplitOpen.value[tx.pk] = false
    delete splitEntries.value[tx.pk]
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
          <v-icon color="primary" class="me-2">mdi-bank-transfer-in</v-icon>
          <span class="text-h6 fw-bold">
            은행 거래내역 자동 수집 & AI 회계 분류 검토
            <v-chip
              size="small"
              :color="mode === 'company' ? 'info' : props.isImprest ? 'teal' : 'primary'"
              class="ms-2 fw-bold"
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
      <v-card-text class="pt-3 pb-2">
        <!-- 연동 계좌(인증서) 상태 안내 배너 / 배지 바 -->
        <v-alert
          v-if="filteredCredentials.length === 0"
          type="warning"
          density="compact"
          variant="tonal"
          class="mb-3 text-caption"
          icon="mdi-alert-circle-outline"
        >
          <div class="d-flex align-center justify-space-between flex-wrap ga-2">
            <div>
              <strong>연동된 계좌(공동인증서)가 없습니다.</strong> 실시간 거래 수집을 위해 먼저 계좌를 연동해 주세요.
            </div>
            <v-btn
              size="x-small"
              color="warning"
              variant="elevated"
              prepend-icon="mdi-link-variant-plus"
              @click="isBankRegisterOpen = true"
            >
              + 계좌/인증서 연동하기
            </v-btn>
          </div>
        </v-alert>

        <div
          v-else
          class="d-flex align-center flex-wrap ga-2 mb-3 pb-2 text-caption text-grey-darken-2 border-b"
        >
          <span class="fw-bold text-grey-darken-3 d-flex align-center">
            <v-icon size="small" color="primary" class="me-1">mdi-shield-check</v-icon>
            연동 현황:
          </span>
          <v-chip
            v-for="info in connectedBankSummary"
            :key="info.bank_code"
            size="x-small"
            color="primary"
            variant="tonal"
            class="fw-medium"
          >
            <v-icon start size="x-small">{{ info.has_cert ? 'mdi-certificate' : 'mdi-flash' }}</v-icon>
            {{ info.bank_name }}: 계좌 {{ info.count }}개 ({{ info.has_cert ? '공동인증서' : '빠른조회' }})
          </v-chip>
          <span class="text-caption text-grey ms-auto">
            (총 {{ filteredCredentials.length }}개 계좌 활성화됨)
          </span>
        </div>

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
                      ? `${getBankName((item as any)?.raw?.bank_code)} | ${(item as any)?.raw?.account_number || ''}`
                      : '모든 연동 계좌의 거래내역 표시'
                  "
                >
                  <template #append>
                    <v-chip
                      v-if="(item as any)?.raw?.auth_type === 'cert'"
                      size="x-small"
                      color="primary"
                      variant="outlined"
                      class="me-1"
                    >
                      <v-icon start size="10">mdi-certificate</v-icon>인증서
                    </v-chip>
                    <v-chip
                      v-else-if="(item as any)?.raw?.auth_type === 'fast'"
                      size="x-small"
                      color="amber-darken-3"
                      variant="outlined"
                      class="me-1"
                    >
                      <v-icon start size="10">mdi-flash</v-icon>빠른조회
                    </v-chip>
                    <v-chip v-if="(item as any)?.raw?.is_imprest" size="x-small" color="teal" variant="flat">
                      운영비 전도금
                    </v-chip>
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
              <th class="text-end" style="width: 110px">금액</th>
              <th class="text-start" style="width: 180px">거래처 / 적요</th>
              <th class="text-start" style="width: 230px">
                {{ mode === 'company' ? '본사 추천 계정과목' : '프로젝트 추천 계정과목' }}
              </th>
              <th v-if="mode === 'project'" class="text-start" style="width: 170px">
                추천 분양계약
              </th>
              <th class="text-start">AI 신뢰도 & 추천 사유</th>
              <th class="text-center" style="width: 90px">승인</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="rawStore.isLoading">
              <td :colspan="mode === 'project' ? 8 : 7" class="text-center py-6 text-grey">
                <v-progress-circular indeterminate color="primary" size="24" class="me-2" />
                거래내역을 불러오는 중입니다...
              </td>
            </tr>
            <tr v-else-if="displayedTransactions.length === 0">
              <td :colspan="mode === 'project' ? 8 : 7" class="text-center py-8 text-grey">
                <div v-if="filteredCredentials.length === 0" class="py-2">
                  <v-icon size="40" color="grey-lighten-1" class="mb-2">mdi-bank-off-outline</v-icon>
                  <div class="fw-bold text-subtitle-2 text-grey-darken-2 mb-1">
                    등록된 은행 연동 계좌(공동인증서)가 없습니다
                  </div>
                  <div class="text-caption text-grey mb-3">
                    공동인증서 또는 신탁 빠른조회 계좌를 연동하면 실시간으로 통장 거래내역을 수집할 수 있습니다.
                  </div>
                  <v-btn
                    size="small"
                    color="primary"
                    variant="elevated"
                    prepend-icon="mdi-link-variant-plus"
                    @click="isBankRegisterOpen = true"
                  >
                    + 새 계좌/인증서 연동하기
                  </v-btn>
                </div>
                <div v-else class="py-2">
                  <v-icon size="40" color="grey-lighten-1" class="mb-2">mdi-file-document-outline</v-icon>
                  <div class="fw-bold text-subtitle-2 text-grey-darken-2 mb-1">
                    조회된 거래내역이 없습니다
                  </div>
                  <div class="text-caption text-grey mb-3">
                    상단의 [전체 일괄 수집] 버튼을 눌러 연동된 은행으로부터 최신 거래내역을 가져오세요.
                  </div>
                </div>
              </td>
            </tr>
            <template
              v-for="tx in displayedTransactions"
              :key="tx.pk"
            >
              <tr :class="{ 'bg-grey-lighten-5': tx.status === 'confirmed' }">
              <!-- 일시 -->
              <td class="text-center text-caption fw-medium">
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
                  class="fw-bold"
                >
                  {{ tx.sort_type === 'deposit' ? '입금' : '출금' }}
                </v-chip>
              </td>

              <!-- 금액 -->
              <td
                class="text-end fw-bold"
                :class="tx.sort_type === 'deposit' ? 'text-primary' : 'text-error'"
              >
                {{ (tx.amount || 0).toLocaleString() }}원
              </td>

              <!-- 거래처 / 적요 -->
              <td class="text-start">
                <div
                  class="fw-bold text-truncate"
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

              <!-- 추천 계정과목 (선택 가능 드롭다운 & 복합 분할 컨트롤) -->
              <td class="text-start">
                <!-- 복합 분개 편집 모드 활성화 시 -->
                <div v-if="tx.status !== 'confirmed' && isSplitOpen[tx.pk]" class="d-flex align-center ga-1">
                  <v-chip size="x-small" color="indigo" variant="flat" class="fw-bold">
                    <v-icon start size="x-small">mdi-call-split</v-icon>
                    {{ splitEntries[tx.pk]?.length || 0 }}개 분개 편집 중
                  </v-chip>
                  <v-btn
                    size="x-small"
                    variant="text"
                    color="grey-darken-1"
                    title="단일 분개로 복귀"
                    @click="cancelSplit(tx)"
                  >
                    취소
                  </v-btn>
                </div>

                <!-- 일반 단일 계정 선택 모드 -->
                <div v-else-if="tx.status !== 'confirmed'">
                  <v-autocomplete
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

                  <!-- 복합 분개 & 이체수수료 빠른 액션 버튼 -->
                  <div class="d-flex align-center ga-1 mt-1">
                    <v-btn
                      v-if="tx.sort_type === 'withdraw'"
                      size="x-small"
                      variant="tonal"
                      color="indigo-darken-1"
                      prepend-icon="mdi-playlist-plus"
                      title="송금액과 이체수수료(500원)를 원클릭으로 분할합니다"
                      @click="quickAddTransferFee(tx)"
                    >
                      +수수료(500원) 분리
                    </v-btn>
                    <v-btn
                      size="x-small"
                      variant="text"
                      color="primary"
                      prepend-icon="mdi-call-split"
                      title="여러 계정으로 복합 분개합니다"
                      @click="toggleSplit(tx)"
                    >
                      복합 분개
                    </v-btn>
                  </div>
                </div>

                <span v-else class="text-caption fw-medium text-success">
                  {{
                    mode === 'company'
                      ? tx.suggested_company_account_name
                      : tx.suggested_project_account_name || '반영 완료'
                  }}
                </span>
              </td>

              <!-- 추천 분양계약 (프로젝트 모드일 때만 표시) -->
              <td v-if="mode === 'project'" class="text-start">
                <div v-if="tx.suggested_contract_name" class="d-flex align-center">
                  <v-icon size="small" color="success" class="me-1">mdi-home-check</v-icon>
                  <span
                    class="text-caption fw-bold text-truncate"
                    style="max-width: 140px"
                  >
                    {{ tx.suggested_contract_name }}
                  </span>
                </div>
                <span v-else class="text-caption text-grey">-</span>
              </td>

              <!-- AI 신뢰도 & 추천 사유 -->
              <td class="text-start">
                <div class="d-flex align-center">
                  <v-chip
                    :color="getScoreColor(tx.confidence_score)"
                    size="x-small"
                    variant="flat"
                    class="fw-bold me-2"
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
                  :color="isSplitOpen[tx.pk] ? 'indigo' : 'primary'"
                  variant="flat"
                  :loading="isConfirming[tx.pk]"
                  :disabled="isSplitOpen[tx.pk] && !isSplitValid(tx)"
                  @click="handleConfirm(tx)"
                >
                  {{ isSplitOpen[tx.pk] ? '분할 승인' : '승인' }}
                </v-btn>
                <v-chip v-else size="x-small" color="grey" variant="tonal"> 완료 </v-chip>
              </td>
            </tr>

            <!-- 복합 거래 분개 분할 패널 (하위 확장 행) -->
            <tr
              v-if="tx.status !== 'confirmed' && isSplitOpen[tx.pk]"
              class="bg-indigo-lighten-5"
            >
              <td :colspan="mode === 'project' ? 8 : 7" class="pa-3">
                <v-card variant="outlined" color="indigo-lighten-3" class="bg-white pa-3 rounded">
                  <div class="d-flex align-center justify-space-between mb-2 flex-wrap ga-2">
                    <div class="d-flex align-center ga-2">
                      <v-icon color="indigo">mdi-call-split</v-icon>
                      <span class="fw-bold text-subtitle-2 text-indigo-darken-3">
                        복합 거래 분개 분할
                      </span>
                      <v-chip size="x-small" color="indigo" variant="tonal">
                        통장 거래금액: {{ (tx.amount || 0).toLocaleString() }}원
                      </v-chip>
                    </div>

                    <div class="d-flex align-center ga-3 flex-wrap">
                      <!-- 차액 실시간 계산 상태 -->
                      <div class="text-caption fw-bold">
                        분개 합계:
                        <span class="text-primary fw-bold">
                          {{ getSplitTotal(tx.pk).toLocaleString() }}원
                        </span>
                        /
                        <span v-if="getSplitDiff(tx) === 0" class="text-success fw-bold">
                          <v-icon size="small" color="success">mdi-check-circle</v-icon> 대차 일치
                        </span>
                        <span v-else class="text-error fw-bold">
                          <v-icon size="small" color="error">mdi-alert-circle</v-icon> 차액:
                          {{ getSplitDiff(tx) > 0 ? '+' : '' }}{{ getSplitDiff(tx).toLocaleString() }}원
                        </span>
                      </div>

                      <v-btn
                        size="x-small"
                        color="indigo"
                        variant="elevated"
                        prepend-icon="mdi-plus"
                        @click="addSplitRow(tx)"
                      >
                        분개 행 추가
                      </v-btn>
                      <v-btn
                        size="x-small"
                        variant="outlined"
                        color="grey-darken-1"
                        @click="cancelSplit(tx)"
                      >
                        분할 취소
                      </v-btn>
                    </div>
                  </div>

                  <!-- 분개 항목 테이블 -->
                  <v-table density="compact" class="border rounded">
                    <thead class="bg-grey-lighten-4">
                      <tr>
                        <th style="width: 45px" class="text-center">#</th>
                        <th style="width: 280px" class="text-start">회계 계정과목 *</th>
                        <th style="width: 180px" class="text-end">분개 금액 (원) *</th>
                        <th class="text-start">거래처 / 적요</th>
                        <th style="width: 55px" class="text-center">삭제</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(entry, eIdx) in splitEntries[tx.pk]" :key="entry.id">
                        <td class="text-center fw-bold text-grey">
                          {{ eIdx + 1 }}
                        </td>
                        <td>
                          <v-autocomplete
                            v-model="entry.account_id"
                            :items="availableAccounts"
                            item-value="value"
                            item-title="title"
                            density="compact"
                            variant="outlined"
                            hide-details
                            clearable
                            placeholder="계정 검색/선택"
                            no-data-text="일치하는 계정과목이 없습니다"
                            :custom-filter="customAccountFilter"
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
                        </td>
                        <td>
                          <v-text-field
                            v-model.number="entry.amount"
                            type="number"
                            min="0"
                            density="compact"
                            variant="outlined"
                            hide-details
                            suffix="원"
                            class="text-end fw-bold"
                          />
                        </td>
                        <td>
                          <v-text-field
                            v-model="entry.trader"
                            density="compact"
                            variant="outlined"
                            hide-details
                            placeholder="거래처명 / 메모"
                          />
                        </td>
                        <td class="text-center">
                          <v-btn
                            icon="mdi-trash-can-outline"
                            size="x-small"
                            variant="text"
                            color="error"
                            :disabled="splitEntries[tx.pk].length <= 1"
                            title="행 삭제"
                            @click="removeSplitRow(tx, eIdx)"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-card>
              </td>
            </tr>
          </template>
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
