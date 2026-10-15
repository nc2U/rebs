<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import type { BulkParseResult } from '@/composables/useBulkTransExcel'

const props = defineProps<{
  modelValue: boolean
  result: BulkParseResult | null
  // 현재 폼에 입력된 거래가 있는지 (있으면 기본값을 '추가'로 둔다)
  hasExisting: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'confirm', payload: { replace: boolean }): void
}>()

const replace = ref(true)
watch(
  () => props.modelValue,
  open => {
    if (open) replace.value = !props.hasExisting
  },
)

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
        <v-alert :type="result.isValid ? 'success' : 'warning'" variant="tonal" class="mb-4">
          <strong>은행거래:</strong> {{ result.summary.transactionCount }}건 |
          <strong>회계 계정:</strong> {{ result.summary.entryCount }}건 |
          <strong class="text-success">정상:</strong> {{ result.summary.validTransactions }}건 |
          <strong class="text-error">오류:</strong> {{ result.summary.invalidTransactions }}건
          <div v-if="!result.isValid" class="mt-1">
            오류가 있는 거래는 반영되지 않습니다. 정상 거래만 폼에 반영할 수 있습니다.
          </div>
        </v-alert>

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
                    <th class="pa-1 text-left">계약자</th>
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
