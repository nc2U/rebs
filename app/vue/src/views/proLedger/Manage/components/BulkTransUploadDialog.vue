<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import type { BulkParseResult } from '@/composables/useBulkTransExcel'

const props = defineProps<{
  modelValue: boolean
  result: BulkParseResult | null
  // 현재 폼에 입력된 거래가 있는지 (있으면 기본값을 '추가'로 둔다)
  hasExisting: boolean
  // 연관 대상 열 이름 (프로젝트: 계약자, 본사: 관계회사(프로젝트))
  relatedLabel?: string
  // 프로젝트 전용: 납부회차 목록
  payOrders?: Array<{ value: number; label: string }>
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirm', payload: { replace: boolean }): void
}>()

const replace = ref(true)
const selectedBulkPayOrder = ref<number | null>(null)

watch(
  () => props.modelValue,
  open => {
    if (open) {
      replace.value = !props.hasExisting
      selectedBulkPayOrder.value = null
    }
  },
)

// 일괄 납부회차 적용
const applyBulkPayOrder = () => {
  if (!props.result || !selectedBulkPayOrder.value || !props.payOrders) return
  const matched = props.payOrders.find(p => p.value === selectedBulkPayOrder.value)
  if (!matched) return

  let appliedCount = 0
  props.result.transactions.forEach(t => {
    t.entries.forEach(e => {
      // 계약자가 있거나 금액이 있는 유효 분개에 회차 적용
      e.installment_order = matched.value
      e.installment_order_name = matched.label
      // 이전 회차 미매칭 경고 제거
      e.warnings = e.warnings.filter(w => !w.includes('납부회차'))
      appliedCount++
    })
  })
}

const validCount = computed(() => props.result?.summary.validTransactions ?? 0)

const handleConfirm = () => {
  emit('confirm', { replace: replace.value })
  emit('update:modelValue', false)
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="1100" persistent scrollable>
    <v-card>
      <v-card-title class="d-flex align-center">
        <span>대량 입력 엑셀 미리보기</span>
        <v-spacer />
        <v-btn icon size="small" @click="emit('update:modelValue', false)">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text v-if="result">
        <v-alert :type="result.isValid ? 'success' : 'warning'" variant="tonal" class="mb-3">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <strong>은행거래:</strong> {{ result.summary.transactionCount }}건 (최대 50건) |
              <strong>회계 계정:</strong> {{ result.summary.entryCount }}건 (최대 200행) |
              <strong class="text-success">정상:</strong> {{ result.summary.validTransactions }}건 |
              <strong class="text-error">오류:</strong> {{ result.summary.invalidTransactions }}건
            </div>
            <v-chip size="x-small" color="primary" variant="outlined" class="ml-auto">
              1회 권장 상한: 50건 / 200행
            </v-chip>
          </div>
          <div v-if="!result.isValid" class="mt-1 text-caption text-error">
            ※ 오류가 있는 거래는 제외되며, 정상 거래만 선택적으로 폼에 반영됩니다.
          </div>
          <div class="mt-1 text-caption text-grey-darken-1">
            ※ 폼에 반영된 데이터는 화면에서 확인 및 수정 후 상단의 [생성] 버튼을 눌러야 최종 저장됩니다.
          </div>
        </v-alert>

        <!-- 중도금 대출 일괄 실행 등 동일 회차 대량 입력 시 편의 기능 -->
        <div
          v-if="payOrders && payOrders.length"
          class="d-flex align-center flex-wrap ga-2 mb-3 pa-2 bg-grey-lighten-4 rounded"
        >
          <v-icon size="18" color="primary">mdi-calendar-check</v-icon>
          <span class="text-caption font-weight-bold">일괄 납부회차 지정:</span>
          <div style="min-width: 240px; max-width: 320px">
            <v-select
              v-model="selectedBulkPayOrder"
              :items="payOrders"
              item-title="label"
              item-value="value"
              density="compact"
              variant="outlined"
              hide-details
              placeholder="적용할 납부회차 선택"
              clearable
            />
          </div>
          <v-btn
            size="small"
            color="primary"
            variant="tonal"
            :disabled="!selectedBulkPayOrder"
            @click="applyBulkPayOrder"
          >
            전체 분개에 일괄 적용
          </v-btn>
          <span class="text-caption text-grey-darken-1">
            (엑셀에 회차가 미기재되었거나 변경이 필요할 때 한 번에 지정할 수 있습니다)
          </span>
        </div>

        <div v-if="result.transactions.length === 0" class="text-center text-grey py-6">
          읽을 수 있는 거래 행이 없습니다. 템플릿 형식을 확인해 주세요.
        </div>

        <div style="max-height: 480px; overflow-y: auto">
          <v-card
            v-for="t in result.transactions"
            :key="t.firstRow"
            variant="outlined"
            class="mb-3"
            :color="t.isValid ? undefined : 'error'"
          >
            <v-card-text class="py-2">
              <div class="d-flex align-center flex-wrap">
                <v-icon
                  :icon="t.isValid ? 'mdi-check-circle' : 'mdi-alert-circle'"
                  :color="t.isValid ? 'success' : 'error'"
                  size="18"
                  class="mr-2"
                />
                <strong class="mr-3">그룹번호 {{ t.key }}</strong>
                <span class="mr-3">{{ t.bankForm.deal_date }}</span>
                <span class="mr-3">{{ t.bankForm.bank_account_name }}</span>
                <span class="mr-3">{{ t.bankForm.sort === 1 ? '입금' : '출금' }}</span>
                <span class="mr-3">{{ t.bankForm.content }}</span>
                <v-spacer />
                <span>
                  거래 {{ (t.bankForm.amount ?? 0).toLocaleString() }} / 분류
                  {{ t.entryTotal.toLocaleString() }}
                </span>
              </div>

              <div v-for="(msg, i) in t.errors" :key="`e${i}`" class="text-error text-caption ml-6">
                ✖ {{ msg }}
              </div>
              <div
                v-for="(msg, i) in t.warnings"
                :key="`w${i}`"
                class="text-warning text-caption ml-6"
              >
                ⚠ {{ msg }}
              </div>

              <table class="w-100 mt-2" style="border-collapse: collapse; font-size: 0.85rem">
                <thead>
                  <tr style="background: #f5f5f5">
                    <th class="pa-1 text-left">행</th>
                    <th class="pa-1 text-left">계정이름</th>
                    <th class="pa-1 text-left">거래처</th>
                    <th class="pa-1 text-right">분류금액</th>
                    <th class="pa-1 text-left">{{ relatedLabel ?? '계약자' }}</th>
                    <th v-if="payOrders && payOrders.length" class="pa-1 text-left">납부회차</th>
                    <th class="pa-1 text-left">검증</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="e in t.entries" :key="e.rowNumber" style="border-top: 1px solid #eee">
                    <td class="pa-1">{{ e.rowNumber }}</td>
                    <td class="pa-1">{{ e.account_name }}</td>
                    <td class="pa-1">{{ e.trader }}</td>
                    <td class="pa-1 text-right">{{ e.amount.toLocaleString() }}</td>
                    <td class="pa-1">{{ e.contract_name }}</td>
                    <td v-if="payOrders && payOrders.length" class="pa-1">
                      <span v-if="e.installment_order_name" class="text-primary font-weight-medium">
                        {{ e.installment_order_name }}
                      </span>
                      <span v-else class="text-grey">-</span>
                    </td>
                    <td class="pa-1">
                      <span v-for="(m, i) in e.errors" :key="`ee${i}`" class="text-error d-block">
                        {{ m }}
                      </span>
                      <span v-for="(m, i) in e.warnings" :key="`ew${i}`" class="text-warning d-block">
                        {{ m }}
                      </span>
                      <span v-if="!e.errors.length && !e.warnings.length" class="text-success">
                        OK
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </v-card-text>
          </v-card>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-switch
          v-model="replace"
          color="primary"
          density="compact"
          hide-details
          :label="replace ? '현재 입력 내용을 대체' : '현재 입력 내용 뒤에 추가'"
          class="ml-3"
        />
        <v-spacer />
        <v-btn variant="tonal" @click="emit('update:modelValue', false)">취소</v-btn>
        <v-btn color="primary" variant="flat" :disabled="validCount === 0" @click="handleConfirm">
          정상 {{ validCount }}건 폼에 반영
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
