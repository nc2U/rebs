<script lang="ts" setup>
import { computed } from 'vue'
import { useProLedger } from '@/store/pinia/proLedger'
import { numFormat } from '@/utils/baseMixins'
import { TableSecondary } from '@/utils/cssMixins'
import type { ProBankTrans } from '@/store/types/proLedger'

interface Props {
  date?: string
}

withDefaults(defineProps<Props>(), {
  date: '',
})

const proLedgerStore = useProLedger()
const dateLedgerTransactions = computed(() => proLedgerStore.dateLedgerTransactions)

const dateIncSet = computed(() =>
  dateLedgerTransactions.value.filter((tx: ProBankTrans) => tx.sort === 1),
)
const dateOutSet = computed(() =>
  dateLedgerTransactions.value.filter((tx: ProBankTrans) => tx.sort === 2),
)

const dateIncTotal = computed(() =>
  dateIncSet.value.reduce((sum: number, tx: ProBankTrans) => sum + (tx.amount || 0), 0),
)
const dateOutTotal = computed(() =>
  dateOutSet.value.reduce((sum: number, tx: ProBankTrans) => sum + (tx.amount || 0), 0),
)

const getFirstEntry = (tx: ProBankTrans) => tx.accounting_entries?.[0]
const getEntryCountSuffix = (tx: ProBankTrans) =>
  tx.accounting_entries && tx.accounting_entries.length > 1
    ? ` 외 ${tx.accounting_entries.length - 1}건`
    : ''
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col style="width: 15%" />
      <col style="width: 30%" />
      <col style="width: 15%" />
      <col style="width: 25%" />
      <col style="width: 15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="4">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 입금내역
          </strong>
          <small class="text-medium-emphasis"> ({{ date }}) 기준 </small>
        </CTableDataCell>
        <CTableDataCell class="text-end">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>계정 과목</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <template v-if="dateIncSet.length > 0">
        <CTableRow v-for="inc in dateIncSet" :key="inc.pk" class="text-center">
          <CTableDataCell>{{ inc.bank_account_name }}</CTableDataCell>
          <CTableDataCell class="text-start">{{ inc.content }}</CTableDataCell>
          <CTableDataCell class="text-end" color="success">
            {{ numFormat(inc.amount) }}
          </CTableDataCell>
          <CTableDataCell class="text-start">
            {{ getFirstEntry(inc)?.account_name ?? '' }}{{ getEntryCountSuffix(inc) }}
          </CTableDataCell>
          <CTableDataCell class="text-start">{{ getFirstEntry(inc)?.trader ?? '' }}</CTableDataCell>
        </CTableRow>
      </template>
      <CTableRow v-else>
        <CTableDataCell colspan="5" class="text-center py-4 text-muted">
          당일 입금 내역이 없습니다.
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-end">
        <CTableHeaderCell class="text-center">합계</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateIncTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>

  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col style="width: 15%" />
      <col style="width: 30%" />
      <col style="width: 15%" />
      <col style="width: 25%" />
      <col style="width: 15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="4">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 출금내역
          </strong>
          <small class="text-medium-emphasis"> ({{ date }}) 기준 </small>
        </CTableDataCell>
        <CTableDataCell class="text-end">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>계정 과목</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <template v-if="dateOutSet.length > 0">
        <CTableRow v-for="out in dateOutSet" :key="out.pk" class="text-center">
          <CTableDataCell>{{ out.bank_account_name }}</CTableDataCell>
          <CTableDataCell class="text-start">{{ out.content }}</CTableDataCell>
          <CTableDataCell class="text-end" color="danger">
            {{ numFormat(out.amount) }}
          </CTableDataCell>
          <CTableDataCell class="text-start">
            {{ getFirstEntry(out)?.account_name ?? '' }}{{ getEntryCountSuffix(out) }}
          </CTableDataCell>
          <CTableDataCell class="text-start">{{ getFirstEntry(out)?.trader ?? '' }}</CTableDataCell>
        </CTableRow>
      </template>
      <CTableRow v-else>
        <CTableDataCell colspan="5" class="text-center py-4 text-muted">
          당일 출금 내역이 없습니다.
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-end">
        <CTableHeaderCell class="text-center">합계</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateOutTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
