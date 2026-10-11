<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRawTransaction } from '@/store/pinia/rawTransaction'
import { useProLedger } from '@/store/pinia/proLedger'
import type { RawBankTransaction } from '@/store/types/rawTransaction'

const props = defineProps<{
  modelValue: boolean
  projectId?: number | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void
  (e: 'confirmed'): void
}>()

const rawStore = useRawTransaction()
const proLedgerStore = useProLedger()

const selectedCredential = ref<number | null>(null)
const selectedStatus = ref<string>('ready')
const selectedAccounts = ref<Record<number, number | null>>({})
const isSyncing = ref<boolean>(false)
const isConfirming = ref<Record<number, boolean>>({})

// 프로젝트 계정과목 목록 (거래 계정만)
const projectAccounts = computed(() =>
  proLedgerStore.proAccounts
    .filter(a => !a.is_cate_only)
    .map(a => ({
      value: a.value,
      title: a.label,
    })),
)

// 고신뢰도(90% 이상) 대기 건수
const highConfidenceCount = computed(() =>
  rawStore.rawTransList.filter(
    t => t.status === 'ready' && t.confidence_score >= 90,
  ).length,
)

const loadData = async () => {
  await rawStore.fetchCredentialList()
  if (rawStore.credentialList.length > 0 && !selectedCredential.value) {
    selectedCredential.value = rawStore.credentialList[0].pk
  }
  await fetchTransactions()
}

const fetchTransactions = async () => {
  await rawStore.fetchRawTransList({
    credential: selectedCredential.value,
    status: selectedStatus.value || undefined,
  })

  // 추천 계정을 로컬 폼 상태로 기본 바인딩
  rawStore.rawTransList.forEach(t => {
    if (t.suggested_project_account) {
      selectedAccounts.value[t.pk] = t.suggested_project_account
    }
  })
}

// 계좌 또는 상태 변경 시 재조회
watch([selectedCredential, selectedStatus], () => {
  fetchTransactions()
})

watch(
  () => props.modelValue,
  val => {
    if (val) loadData()
  },
)

// 즉시 은행 수집 실행
const handleSync = async () => {
  if (!selectedCredential.value) return
  isSyncing.value = true
  try {
    await rawStore.syncCredential(selectedCredential.value)
    await fetchTransactions()
  } finally {
    isSyncing.value = false
  }
}

// 단건 승인
const handleConfirm = async (tx: RawBankTransaction) => {
  isConfirming.value[tx.pk] = true
  try {
    const customAccount = selectedAccounts.value[tx.pk] || tx.suggested_project_account
    await rawStore.confirmRawTransaction(tx.pk, customAccount, tx.suggested_contract)
    await fetchTransactions()
    emit('confirmed')
  } finally {
    isConfirming.value[tx.pk] = false
  }
}

// 90% 이상 고신뢰도 일괄 승인
const handleBulkConfirm = async () => {
  if (highConfidenceCount.value === 0) return
  if (!confirm(`신뢰도 90% 이상인 ${highConfidenceCount.value}건의 거래를 일괄 승인하시겠습니까?`)) return

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
    max-width="1300"
    scrollable
    @update:model-value="emit('update:modelValue', $event)"
  >
    <v-card class="pa-2">
      <!-- 헤더 -->
      <v-card-title class="d-flex align-center justify-space-between pb-2 border-b">
        <div class="d-flex align-center">
          <v-icon color="primary" class="mr-2">mdi-bank-transfer-in</v-icon>
          <span class="text-h6 font-weight-bold">은행 거래내역 자동 수집 및 AI 회계 분류 검토</span>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="emit('update:modelValue', false)" />
      </v-card-title>

      <!-- 툴바 컨트롤러 -->
      <v-card-text class="pt-4 pb-2">
        <v-row dense align="center">
          <v-col cols="12" sm="4" md="3">
            <v-select
              v-model="selectedCredential"
              :items="rawStore.credentialList"
              item-title="account_alias"
              item-value="pk"
              label="연동 계좌 선택"
              density="compact"
              variant="outlined"
              hide-details
            >
              <template #item="{ props: itemProps, item }">
                <v-list-item v-bind="itemProps" :subtitle="`${(item as any).raw?.bank_code || ''} | ${(item as any).raw?.account_number || ''}`" />
              </template>
            </v-select>
          </v-col>

          <v-col cols="12" sm="3" md="2">
            <v-select
              v-model="selectedStatus"
              :items="[
                { title: '컨펌 대기 (Ready)', value: 'ready' },
                { title: 'AI 분류 대기 (Pending)', value: 'pending' },
                { title: '승인 완료 (Confirmed)', value: 'confirmed' },
                { title: '전체 보기', value: '' },
              ]"
              density="compact"
              variant="outlined"
              hide-details
            />
          </v-col>

          <v-col cols="12" sm="5" md="7" class="d-flex justify-end ga-2">
            <v-btn
              color="primary"
              variant="tonal"
              density="compact"
              prepend-icon="mdi-cloud-sync"
              :loading="isSyncing"
              @click="handleSync"
            >
              은행 최신거래 수집
            </v-btn>

            <v-btn
              color="success"
              variant="elevated"
              density="compact"
              prepend-icon="mdi-check-all"
              :disabled="highConfidenceCount === 0"
              @click="handleBulkConfirm"
            >
              고신뢰도 일괄 승인 ({{ highConfidenceCount }}건)
            </v-btn>
          </v-card-text>

          <!-- 메인 데이터 테이블 -->
          <v-table density="compact" hover class="border mt-2">
            <thead class="bg-grey-lighten-4">
              <tr>
                <th class="text-center" style="width: 100px">거래일시</th>
                <th class="text-center" style="width: 70px">구분</th>
                <th class="text-right" style="width: 110px">금액</th>
                <th class="text-left" style="width: 180px">거래처 / 적요</th>
                <th class="text-left" style="width: 220px">AI 추천 계정과목</th>
                <th class="text-left" style="width: 160px">추천 분양계약</th>
                <th class="text-left">AI 신뢰도 & 추천 사유</th>
                <th class="text-center" style="width: 90px">승인</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="rawStore.isLoading">
                <td colspan="8" class="text-center py-6 text-grey">
                  <v-progress-circular indeterminate color="primary" size="24" class="mr-2" />
                  거래내역을 불러오는 중입니다...
                </td>
              </tr>
              <tr v-else-if="rawStore.rawTransList.length === 0">
                <td colspan="8" class="text-center py-6 text-grey">
                  조회된 거래내역이 없습니다.
                </td>
              </tr>
              <tr
                v-for="tx in rawStore.rawTransList"
                :key="tx.pk"
                :class="{ 'bg-grey-lighten-5': tx.status === 'confirmed' }"
              >
                <!-- 일시 -->
                <td class="text-center text-caption font-weight-medium">
                  <div>{{ tx.deal_date }}</div>
                  <div class="text-grey text-caption" style="font-size: 11px">{{ tx.deal_time || '' }}</div>
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
                  {{ tx.amount.toLocaleString() }}원
                </td>

                <!-- 거래처 / 적요 -->
                <td>
                  <div class="font-weight-medium text-truncate" style="max-width: 180px">
                    {{ tx.client_name || tx.content || '-' }}
                  </div>
                  <div class="text-grey text-caption text-truncate" style="font-size: 11px; max-width: 180px">
                    {{ tx.content && tx.client_name ? tx.content : tx.branch_name }}
                  </div>
                </td>

                <!-- AI 추천 계정과목 선택 드롭다운 -->
                <td>
                  <div v-if="tx.status === 'confirmed'" class="text-caption font-weight-medium text-grey-darken-1">
                    {{ tx.suggested_project_account_name || '계정 반영완료' }}
                  </div>
                  <v-select
                    v-else
                    v-model="selectedAccounts[tx.pk]"
                    :items="projectAccounts"
                    density="compact"
                    variant="outlined"
                    hide-details
                    placeholder="계정 선택"
                    style="min-width: 180px; font-size: 12px"
                  />
                </td>

                <!-- 추천 분양계약 (동호수) -->
                <td>
                  <div v-if="tx.suggested_contract_name" class="d-flex align-center">
                    <v-icon size="14" color="info" class="mr-1">mdi-file-document-check-outline</v-icon>
                    <span class="text-caption font-weight-medium text-blue-darken-2">
                      {{ tx.suggested_contract_name }}
                    </span>
                  </div>
                  <span v-else class="text-caption text-grey">-</span>
                </td>

                <!-- AI 신뢰도 & 추천 사유 -->
                <td>
                  <div class="d-flex align-center ga-1">
                    <v-chip
                      :color="getScoreColor(tx.confidence_score)"
                      size="x-small"
                      variant="flat"
                      class="font-weight-bold"
                    >
                      {{ tx.confidence_score }}%
                    </v-chip>
                    <span class="text-caption text-grey-darken-2 text-truncate" style="max-width: 250px">
                      {{ tx.ai_reason }}
                    </span>
                  </div>
                </td>

                <!-- 승인 버튼 -->
                <td class="text-center">
                  <v-chip v-if="tx.status === 'confirmed'" color="grey" size="x-small" variant="outlined">
                    승인완료
                  </v-chip>
                  <v-btn
                    v-else
                    color="primary"
                    size="x-small"
                    variant="flat"
                    :loading="isConfirming[tx.pk]"
                    @click="handleConfirm(tx)"
                  >
                    승인
                  </v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card-text>
      </v-card>
  </v-dialog>
</template>
