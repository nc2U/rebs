<script lang="ts" setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import { headerSecondary } from '@/utils/cssMixins'

const store = useStore()
const props = defineProps({ date: String })

const preBalance = ref(0)
const dateIncSum = ref(0)
const dateOutSum = ref(0)
const dateBalance = ref(0)

const comBalanceByAccList = computed(
  () => store.state.comCash.comBalanceByAccList,
)

const getSumTotal = () => {
  const _dateIncSum =
    comBalanceByAccList.value.length !== 0
      ? comBalanceByAccList.value
          .map((i: any) => i.date_inc)
          .reduce((x: number, y: number) => x + y)
      : 0
  const _dateOutSum =
    comBalanceByAccList.value.length !== 0
      ? comBalanceByAccList.value
          .map((o: any) => o.date_out)
          .reduce((x: number, y: number) => x + y)
      : 0
  const _dateIncTotal =
    comBalanceByAccList.value.length !== 0
      ? comBalanceByAccList.value
          .filter((i: any) => i.inc_sum !== null)
          .map((i: any) => i.inc_sum)
          .reduce((x: number, y: number) => x + y)
      : 0
  const _dateOutTotal =
    comBalanceByAccList.value.length !== 0
      ? comBalanceByAccList.value
          .filter((o: any) => o.out_sum !== null)
          .map((o: any) => o.out_sum)
          .reduce((x: number, y: number) => x + y)
      : 0
  dateIncSum.value = _dateIncSum
  dateOutSum.value = _dateOutSum
  dateBalance.value = _dateIncTotal - _dateOutTotal
  preBalance.value = _dateIncTotal - _dateOutTotal - (_dateIncSum - _dateOutSum)
}

onMounted(() => getSumTotal())
watch(comBalanceByAccList, () => getSumTotal())
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="10%" />
      <col width="30%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 계좌별 자금현황
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 현재
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell colspan="2">구분</CTableHeaderCell>
        <CTableHeaderCell>전일잔고</CTableHeaderCell>
        <CTableHeaderCell>금일입금(증가)</CTableHeaderCell>
        <CTableHeaderCell>금일출금(감소)</CTableHeaderCell>
        <CTableHeaderCell>금일잔고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow
        v-for="(bal, i) in comBalanceByAccList"
        :key="i"
        class="text-right"
      >
        <CTableDataCell
          v-if="i === 0"
          class="text-center"
          :rowspan="comBalanceByAccList.length"
        >
          보통예금
        </CTableDataCell>
        <CTableDataCell class="text-left">{{ bal.bank_acc }}</CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(bal.inc_sum - bal.out_sum - (bal.date_inc - bal.date_out))
          }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(bal.date_inc) }}</CTableDataCell>
        <CTableDataCell>{{ numFormat(bal.date_out) }}</CTableDataCell>
        <CTableDataCell>
          {{ numFormat(bal.inc_sum - bal.out_sum) }}
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="headerSecondary" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          현금성 자산 계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(preBalance) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateIncSum) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateOutSum) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateBalance) }}</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
