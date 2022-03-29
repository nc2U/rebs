<template>
  <h6>계약해지 현황</h6>

  <CTable hover responsive align="middle">
    <colgroup>
      <col width="20%" />
      <col width="10%" />
      <col width="15%" />
      <col width="10%" />
      <col width="15%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
    </colgroup>

    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell rowspan="2">계약 해지자</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">현재상태</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">환불(예정)금액</CTableHeaderCell>
        <CTableHeaderCell colspan="3">환불계좌</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">해지신청일</CTableHeaderCell>
        <CTableHeaderCell rowspan="2">환불처리일</CTableHeaderCell>
      </CTableRow>
      <CTableRow>
        <CTableHeaderCell>은행명</CTableHeaderCell>
        <CTableHeaderCell>계좌번호</CTableHeaderCell>
        <CTableHeaderCell>예금주</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody class="text-center">
      <CTableRow v-for="cont in contReleaseList" :key="cont.pk">
        <CTableDataCell>{{ cont.contractor }}</CTableDataCell>
        <CTableDataCell>{{ cont.status }}</CTableDataCell>
        <CTableDataCell class="text-right">
          {{ numFormat(cont.refund_amount) }}
        </CTableDataCell>
        <CTableDataCell class="text-left">
          {{ cont.refund_account_bank }}
        </CTableDataCell>
        <CTableDataCell class="text-left">
          {{ cont.refund_account_number }}
        </CTableDataCell>
        <CTableDataCell>{{ cont.refund_account_depositor }}</CTableDataCell>
        <CTableDataCell>{{ cont.request_date }}</CTableDataCell>
        <CTableDataCell>{{ cont.completion_date }}</CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>

  <CSmartPagination
    :activePage="1"
    :limit="8"
    :pages="releasePages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'CanceledList',
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    ...mapState('contract', ['contReleaseList']),
    ...mapGetters('contract', ['releasePages']),
  },
  methods: {
    pageSelect(page: number) {
      this.$emit('page-select', page)
    },
  },
})
</script>
