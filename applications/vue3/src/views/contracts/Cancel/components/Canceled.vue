<template>
  <CTableDataCell>
    {{ cutString(cont.contractor.__str__, 25) }}
  </CTableDataCell>
  <CTableDataCell>{{ getStatus(cont.status) }}</CTableDataCell>
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
  <CTableDataCell>
    <CButton type="button" color="success" size="sm">확인</CButton>
  </CTableDataCell>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Canceled',
  props: { cont: Object },
  methods: {
    getStatus(num: string) {
      const status = [
        { code: '0', text: '신청 취소' },
        { code: '3', text: '신청 중' },
        { code: '4', text: '처리완료' },
        { code: '5', text: '자격상실(제명)' },
      ]
      return status.filter(s => s.code === num).map(s => s.text)[0]
    },
  },
})
</script>
