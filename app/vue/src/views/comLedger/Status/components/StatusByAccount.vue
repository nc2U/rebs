<script lang="ts" setup>
import { computed } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { useComLedger } from '@/store/pinia/comLedger'
import { TableSecondary } from '@/utils/cssMixins'

interface Props {
  date?: string
  isBalance?: string
}

withDefaults(defineProps<Props>(), {
  date: '',
  isBalance: 'true',
})

const emit = defineEmits<{
  (e: 'is-exist-balance', val: boolean): void
}>()

const ledgerStore = useComLedger()
const comBalanceByAccList = computed(() => ledgerStore.comLedgerBalanceByAccList)

const totals = computed(() => {
  let dateIncSum = 0
  let dateOutSum = 0
  let dateIncTotal = 0
  let dateOutTotal = 0

  for (const bal of comBalanceByAccList.value) {
    dateIncSum += (bal as any).date_inc || 0
    dateOutSum += (bal as any).date_out || 0
    if ((bal as any).inc_sum !== null && (bal as any).inc_sum !== undefined) {
      dateIncTotal += (bal as any).inc_sum || 0
    }
    if ((bal as any).out_sum !== null && (bal as any).out_sum !== undefined) {
      dateOutTotal += (bal as any).out_sum || 0
    }
  }

  const dateBalance = dateIncTotal - dateOutTotal
  const preBalance = dateBalance - (dateIncSum - dateOutSum)

  return {
    preBalance,
    dateIncSum,
    dateOutSum,
    dateBalance,
  }
})

const handleExistBalanceChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  emit('is-exist-balance', target.checked)
}
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col style="width: 8%" />
      <col style="width: 16%" />
      <col style="width: 16%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="2">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 계좌별 자금현황
          </strong>
          <small class="text-medium-emphasis"> ({{ date }}) 현재 </small>
        </CTableDataCell>
        <CTableDataCell colspan="4">
          <CFormSwitch
            id="select-acc-sort"
            label="잔고 존재 계좌"
            :checked="!!isBalance"
            @change="handleExistBalanceChange"
          />
        </CTableDataCell>
        <CTableDataCell class="text-end">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell colspan="3">계좌 구분</CTableHeaderCell>
        <CTableHeaderCell>전일잔고</CTableHeaderCell>
        <CTableHeaderCell>금일입금(증가)</CTableHeaderCell>
        <CTableHeaderCell>금일출금(감소)</CTableHeaderCell>
        <CTableHeaderCell>금일잔고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <template v-if="comBalanceByAccList.length > 0">
        <CTableRow v-for="(bal, i) in comBalanceByAccList" :key="i" class="text-end">
          <CTableDataCell v-if="i === 0" class="text-center" :rowspan="comBalanceByAccList.length">
            보통예금
          </CTableDataCell>
          <CTableDataCell class="text-start">{{ bal.bank_acc }}</CTableDataCell>
          <CTableDataCell class="text-start">{{ bal.bank_num }}</CTableDataCell>
          <CTableDataCell>
            {{ numFormat(((bal as any).inc_sum || 0) - ((bal as any).out_sum || 0) - ((bal as any).date_inc - (bal as any).date_out)) }}
          </CTableDataCell>
          <CTableDataCell>{{ numFormat((bal as any).date_inc) }}</CTableDataCell>
          <CTableDataCell>{{ numFormat((bal as any).date_out) }}</CTableDataCell>
          <CTableDataCell>
            {{ numFormat(((bal as any).inc_sum || 0) - ((bal as any).out_sum || 0)) }}
          </CTableDataCell>
        </CTableRow>
      </template>
      <CTableRow v-else>
        <CTableDataCell colspan="7" class="text-center py-4 text-muted">
          조회된 계좌별 자금 현황이 없습니다.
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-end">
        <CTableHeaderCell colspan="3" class="text-center"> 현금성 자산 계</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totals.preBalance) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totals.dateIncSum) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totals.dateOutSum) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totals.dateBalance) }}</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
