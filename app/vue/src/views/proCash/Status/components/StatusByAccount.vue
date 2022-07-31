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
            프로젝트 계좌별 자금현황
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 현재
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="secondary" class="text-center">
        <CTableHeaderCell colspan="2">구분</CTableHeaderCell>
        <CTableHeaderCell>전일잔고</CTableHeaderCell>
        <CTableHeaderCell>금일입금(증가)</CTableHeaderCell>
        <CTableHeaderCell>금일출금(감소)</CTableHeaderCell>
        <CTableHeaderCell>금일잔고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow
        class="text-right"
        v-for="(bal, i) in balanceByAccList"
        :key="i"
      >
        <CTableDataCell
          class="text-center"
          :rowspan="balanceByAccList.length"
          v-if="i === 0"
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

      <CTableRow color="secondary" class="text-right">
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

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'StatusByAccount',
  components: {},
  props: { date: String },
  data() {
    return {
      preBalance: 0,
      dateIncSum: 0,
      dateOutSum: 0,
      dateBalance: 0,
    }
  },
  created() {
    this.getSumTotal()
  },
  computed: {
    ...mapState('proCash', ['balanceByAccList']),
  },
  watch: {
    balanceByAccList() {
      this.getSumTotal()
    },
  },
  methods: {
    getSumTotal() {
      const dateIncSum =
        this.balanceByAccList.length !== 0
          ? this.balanceByAccList
              .map((i: any) => i.date_inc)
              .reduce((x: number, y: number) => x + y)
          : 0
      const dateOutSum =
        this.balanceByAccList.length !== 0
          ? this.balanceByAccList
              .map((o: any) => o.date_out)
              .reduce((x: number, y: number) => x + y)
          : 0
      const dateIncTotal =
        this.balanceByAccList.length !== 0
          ? this.balanceByAccList
              .filter((i: any) => i.inc_sum !== null)
              .map((i: any) => i.inc_sum)
              .reduce((x: number, y: number) => x + y)
          : 0
      const dateOutTotal =
        this.balanceByAccList.length !== 0
          ? this.balanceByAccList
              .filter((o: any) => o.out_sum !== null)
              .map((o: any) => o.out_sum)
              .reduce((x: number, y: number) => x + y)
          : 0
      this.dateIncSum = dateIncSum
      this.dateOutSum = dateOutSum
      this.dateBalance = dateIncTotal - dateOutTotal
      this.preBalance = dateIncTotal - dateOutTotal - (dateIncSum - dateOutSum)
    },
  },
})
</script>
