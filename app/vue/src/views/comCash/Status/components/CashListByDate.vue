<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="14%" />
      <col width="15%" />
      <col width="15%" />
      <col width="20%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="6">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 당일 입금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="secondary" class="text-center">
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>계정</CTableHeaderCell>
        <CTableHeaderCell>세부 계정</CTableHeaderCell>
        <CTableHeaderCell>입금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="inc in dateIncSet" :key="inc.pk">
        <CTableDataCell>
          {{ getDAccText(inc.account_d1, listAccD1List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(inc.account_d2, listAccD2List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(inc.account_d3, listAccD3List) }}
        </CTableDataCell>
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
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="success"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow color="secondary" class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
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
      <col width="12%" />
      <col width="12%" />
      <col width="12%" />
      <col width="14%" />
      <col width="15%" />
      <col width="15%" />
      <col width="20%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="6">
          <strong>
            <CIcon name="cilFolderOpen" />
            본사 당일 출금내역
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow color="secondary" class="text-center">
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>계정</CTableHeaderCell>
        <CTableHeaderCell>세부 계정</CTableHeaderCell>
        <CTableHeaderCell>출금 금액</CTableHeaderCell>
        <CTableHeaderCell>거래 계좌</CTableHeaderCell>
        <CTableHeaderCell>거래처</CTableHeaderCell>
        <CTableHeaderCell>적요</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow class="text-center" v-for="out in dateOutSet" :key="out.pk">
        <CTableDataCell>
          {{ getDAccText(out.account_d1, listAccD1List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(out.account_d2, listAccD2List) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ getDAccText(out.account_d3, listAccD3List) }}
        </CTableDataCell>
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
        <CTableDataCell></CTableDataCell>
        <CTableDataCell color="danger"></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
        <CTableDataCell></CTableDataCell>
      </CTableRow>

      <CTableRow color="secondary" class="text-right">
        <CTableHeaderCell colspan="3" class="text-center">
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
    ...mapState('comCash', [
      'listAccD1List',
      'listAccD2List',
      'listAccD3List',
      'comBankList',
      'dateCashBook',
    ]),
  },
  watch: {
    dateCashBook() {
      this.setData()
    },
  },
  methods: {
    getDAccText(num: number, acc: any) {
      return acc.filter((d: any) => d.pk === num).map((d: any) => d.name)[0]
    },
    getBankAcc(num: number) {
      return this.comBankList
        .filter((b: any) => b.pk === num)
        .map((b: any) => b.alias_name)[0]
    },
    setData(this: any) {
      this.dateIncSet = this.dateCashBook.filter(
        (i: any) => i.income > 0 && !i.outlay,
      )
      this.dateOutSet = this.dateCashBook.filter(
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
