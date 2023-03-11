<script lang="ts" setup>
import { computed } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { TableSecondary } from '@/utils/cssMixins'
import Payment from '@/views/payments/List/components/Payment.vue'
import Pagination from '@/components/Pagination'

const emit = defineEmits(['page-select'])

const paymentStore = usePayment()
const getPayments = computed(() => paymentStore.getPayments)
const paymentPages = computed(() => paymentStore.paymentPages)

const pageSelect = (page: number) => emit('page-select', page)
</script>

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
      <CTableRow :color="TableSecondary" class="text-center">
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
