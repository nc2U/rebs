<template>
  <CTable hover responsive>
    <colgroup>
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
    </colgroup>

    <CTableHead>
      <CTableRow color="dark">
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
      <Payment />
    </CTableBody>
  </CTable>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="itemsPerPage(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Payment from '@/views/payments/List/components/Payment.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ContractList',
  components: { Payment },
  props: { project: Object },
  computed: {
    ...mapGetters('contract', ['contractIndex', 'itemsPerPage']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
  },
})
</script>
