<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 입금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="secondary" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="inc in dateIncSet" :key="inc.pk">
        <CTableDataCell>{{ getD1Text(inc.project_account_d1) }}</CTableDataCell>
        <CTableDataCell>{{ getD2Text(inc.project_account_d2) }}</CTableDataCell>
        <CTableDataCell class="text-right" color="success">
          {{ numFormat(inc.income) }}
        </CTableDataCell>
        <CTableDataCell>{{ getBankAcc(inc.bank_account) }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ inc.trader }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ inc.content }}</CTableDataCell>
      </CTableRow>

      <CTableRow class="text-center">
        <CTableDataCell>&nbsp;</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="success"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow color="secondary" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateIncTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>

  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="15%" />
      <col width="25%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="5">
          <strong>
            <CIcon name="cilFolderOpen" />
            프로젝트 당일 출금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="secondary" class="text-center">
        <CTableHeaderCell>항목</CTableHeaderCell>
        <CTableHeaderCell>세부 항목</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="out in dateOutSet" :key="out.pk">
        <CTableDataCell>{{ getD1Text(out.project_account_d1) }}</CTableDataCell>
        <CTableDataCell>{{ getD2Text(out.project_account_d2) }}</CTableDataCell>
        <CTableDataCell class="text-right" color="danger">
          {{ numFormat(out.outlay) }}
        </CTableDataCell>
        <CTableDataCell>{{ getBankAcc(out.bank_account) }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ out.trader }}</CTableDataCell>
        <CTableDataCell class="text-left">{{ out.content }}</CTableDataCell>
      </CTableRow>
      <CTableRow class="text-center">
        <CTableDataCell>&nbsp;</CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="danger"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow color="secondary" class="text-right">
        <CTableHeaderCell colspan="2" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(dateOutTotal) }}</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'CashListByDate',
  components: {},
  props: { date: String },
  setup() {
    return {}
  },
  data() {
    return {
      dateIncSet: null,
      dateOutSet: null,
      dateIncTotal: 0,
      dateOutTotal: 0,
    }
  },
  created(this: any) {
    this.setData()
  },
  computed: {
    ...mapState('proCash', [
      'allAccD1List',
      'allAccD2List',
      'proBankAccountList',
      'proDateCashBook',
    ]),
  },
  watch: {
    proDateCashBook() {
      this.setData()
    },
  },
  methods: {
    getD1Text(num: number) {
      return this.allAccD1List
        .filter((d: any) => d.pk === num)
        .map((d: any) => d.name)[0]
    },
    getD2Text(num: number) {
      return this.allAccD2List
        .filter((d: any) => d.pk === num)
        .map((d: any) => d.name)[0]
    },
    getBankAcc(num: number) {
      return this.proBankAccountList
        .filter((b: any) => b.pk === num)
        .map((b: any) => b.alias_name)[0]
    },
    setData(this: any) {
      this.dateIncSet = this.proDateCashBook.filter(
        (i: any) => i.income > 0 && !i.outlay,
      )
      this.dateOutSet = this.proDateCashBook.filter(
        (o: any) => o.outlay > 0 && !o.income,
      )
      this.dateIncTotal = this.dateIncSet
        .map((i: any) => i.income)
        .reduce((x: number, y: number) => x + y, 0)
      this.dateOutTotal = this.dateOutSet
        .map((o: any) => o.outlay)
        .reduce((x: number, y: number) => x + y, 0)
    },
  },
})
</script>
