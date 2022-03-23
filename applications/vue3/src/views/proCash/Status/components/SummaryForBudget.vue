<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="5%" />
      <col width="10%" />
      <col width="10%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="8">
          <strong>
            <CIcon name="cilFolderOpen" />
            사업예산 및 집행현황
          </strong>
          <small>({{ dateFormat(date) }}) 기준</small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="dark" class="text-center">
        <CTableHeaderCell colspan="4">구분</CTableHeaderCell>
        <CTableHeaderCell>예산액</CTableHeaderCell>
        <CTableHeaderCell>전월 집행금액 누계</CTableHeaderCell>
        <CTableHeaderCell>당월 집행금액</CTableHeaderCell>
        <CTableHeaderCell>집행금액 합계</CTableHeaderCell>
        <CTableHeaderCell>가용(잔여) 예산합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow
        class="text-right"
        v-for="(bdj, i) in proBudgetList"
        :key="bdj.pk"
      >
        <CTableDataCell
          color="info"
          class="text-center"
          :rowspan="proBudgetList.length"
          v-if="i === 0"
        >
          사업비
        </CTableDataCell>
        <CTableDataCell
          class="text-center"
          :rowspan="getLength(bdj.account_d1.acc_d2s)"
          v-if="getFirst(bdj.account_d1.acc_d2s) === bdj.account_d2.pk"
        >
          {{ bdj.account_d1.name }}
        </CTableDataCell>
        <CTableDataCell
          class="text-left"
          :rowspan="getSubTitle(bdj.account_d2.sub_title).length"
          v-if="
            bdj.account_d2.sub_title &&
            bdj.pk === getSubTitle(bdj.account_d2.sub_title)[0]
          "
        >
          {{ bdj.account_d2.sub_title }}
        </CTableDataCell>
        <CTableDataCell
          class="text-left"
          :colspan="bdj.account_d2.sub_title ? 1 : 2"
        >
          {{ bdj.account_d2.name }}
        </CTableDataCell>
        <CTableDataCell>{{ numFormat(bdj.budget) }}</CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              getEASum(bdj.account_d2.pk) - getEAMonth(bdj.account_d2.pk),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEAMonth(bdj.account_d2.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEASum(bdj.account_d2.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell
          :class="bdj.budget < getEASum(bdj.account_d2.pk) ? 'text-danger' : ''"
        >
          {{ numFormat(bdj.budget - (getEASum(bdj.account_d2.pk) || 0)) }}
        </CTableDataCell>
      </CTableRow>

      <CTableRow color="dark" class="text-right">
        <CTableHeaderCell colspan="4" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totalBudget) }}</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
        <CTableHeaderCell>-</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'SummaryForBudget',
  props: { date: String },
  data() {
    return {
      totalBudget: 1,
    }
  },
  // created() {
  //   alert('a')
  // },
  computed: {
    ...mapState('contract', ['orderGroupList']),
    ...mapState('project', ['unitTypeList']),
    ...mapState('proCash', ['proBudgetList', 'execAmountList']),
  },
  watch: {
    proBudgetList(val: any) {
      console.log(val)
      this.totalBudget = val.length // !== 0
      // ? 100 // val
      // : // .map((b: any) => b.budget)
      // .reduce((x: number, y: number) => x + y)
      // 10
    },
  },
  methods: {
    getD2sInter(arr: number[]) {
      const d2s = this.proBudgetList.map((b: any) => b.account_d2.pk)
      const d2Inters = arr.filter(x => d2s.includes(x))
      return d2Inters
    },
    getLength(arr: number[]) {
      return this.getD2sInter(arr).length
    },
    getFirst(arr: number[]) {
      return this.getD2sInter(arr)[0]
    },
    getSubTitle(sub: string) {
      return sub !== ''
        ? this.proBudgetList
            .filter((b: any) => b.account_d2.sub_title === sub)
            .map((b: any) => b.pk)
        : []
    },
    getExecAmount(d2: number) {
      return this.execAmountList.filter((e: any) => e.acc_d2 === d2)
    },
    getEASum(d2: number) {
      return this.getExecAmount(d2).map((e: any) => e.all_sum)[0]
    },
    getEAMonth(d2: number) {
      return this.getExecAmount(d2).map((e: any) => e.month_sum)[0]
    },
  },
})
</script>
