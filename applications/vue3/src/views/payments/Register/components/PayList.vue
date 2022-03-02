<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="16%" />
      <col width="18%" />
      <col width="16%" />
      <col width="22%" />
      <col width="18%" />
      <col width="10%" />
    </colgroup>

    <CTableHead color="dark">
      <CTableRow class="text-center">
        <CTableHeaderCell>수납일자</CTableHeaderCell>
        <CTableHeaderCell>납부회차</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>수납계좌</CTableHeaderCell>
        <CTableHeaderCell>입금자명</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <CTableRow class="text-center" v-for="pay in paymentList" :key="pay.pk">
        <CTableDataCell>{{ pay.deal_date }}</CTableDataCell>
        <CTableDataCell>{{ pay.installment_order }}</CTableDataCell>
        <CTableDataCell class="text-right">
          {{ numFormat(pay.income) }}
        </CTableDataCell>
        <CTableDataCell>{{ pay.bank_account }}</CTableDataCell>
        <CTableDataCell>{{ pay.trader }}</CTableDataCell>
        <CTableDataCell>
          <CButton type="button" color="info" size="sm">보기</CButton>
        </CTableDataCell>
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="dark" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>
          {{ numFormat(paymentSum) }}
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'PayList',
  components: {},
  props: { contract: Object },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    paymentSum() {
      return this.paymentList.length !== 0
        ? this.paymentList
            .map((p: any) => p.income)
            .reduce((x: any, y: any) => x + y)
        : 0
    },
    ...mapState('payment', ['paymentList']),
  },
  methods: {},
})
</script>
