<template>
  <CTable hover responsive align="middle">
    <colgroup>
      <col width="10%" />
      <col width="10%" />
      <col width="8%" />
      <col width="9%" />
      <col width="8%" />
      <col width="9%" />
      <col width="14%" />
      <col width="13%" />
      <col width="13%" />
      <col width="6%" />
    </colgroup>

    <CTableHead>
      <CTableRow :color="headerSecondary" class="text-center">
        <CTableHeaderCell scope="col">거래일자</CTableHeaderCell>
        <CTableHeaderCell scope="col">차수</CTableHeaderCell>
        <CTableHeaderCell scope="col">타입</CTableHeaderCell>
        <CTableHeaderCell scope="col">일련번호</CTableHeaderCell>
        <CTableHeaderCell scope="col">계약자</CTableHeaderCell>
        <CTableHeaderCell scope="col">수납금액</CTableHeaderCell>
        <CTableHeaderCell scope="col">납입회차</CTableHeaderCell>
        <CTableHeaderCell scope="col">수납계좌</CTableHeaderCell>
        <CTableHeaderCell scope="col">입금자</CTableHeaderCell>
        <CTableHeaderCell scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Payment
        v-for="(payment, i) in getPayments"
        :key="i"
        :payment="payment"
        @on-update="onUpdate"
        @on-patch="onPatch"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    :active-page="1"
    :limit="8"
    :pages="paymentPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Payment from '@/views/payments/List/components/Payment.vue'
import Pagination from '@/components/Pagination'
import { headerSecondary } from '@/utils/cssMixins'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'PaymentList',
  components: { Payment, Pagination },
  props: { project: Object },
  computed: {
    headerSecondary() {
      return headerSecondary.value
    },
    ...mapGetters('payment', ['paymentPages', 'getPayments']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
    onUpdate(payload: any) {
      this.$emit('on-update', payload)
    },
    onPatch(payload: any) {
      this.$emit('on-patch', payload)
    },
    onDelete(pk: number) {
      this.$emit('on-delete', pk)
    },
  },
})
</script>
