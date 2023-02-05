<script lang="ts" setup>
import { computed } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { DownPay as dp } from '@/store/types/payment'
import { TableSecondary } from '@/utils/cssMixins'
import DownPay from '@/views/projects/DownPay/components/DownPay.vue'

defineProps({
  orders: { type: Object, default: null },
  types: { type: Object, default: null },
})
const emit = defineEmits(['on-update', 'on-delete'])

const paymentStore = usePayment()
const downPayList = computed(() => paymentStore.downPayList)

const onUpdateDownPay = (payload: dp) => emit('on-update', payload)
const onDeleteDownPay = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
      <col width="25%" />
    </colgroup>
    <CTableHead :color="TableSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>차수</CTableHeaderCell>
        <CTableHeaderCell>타입</CTableHeaderCell>
        <CTableHeaderCell>분할 납부회수</CTableHeaderCell>
        <CTableHeaderCell>회별 납부금액</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="downPayList.length > 0">
      <DownPay
        v-for="downPay in downPayList"
        :key="downPay.pk"
        :down-pay="downPay"
        :orders="orders"
        :types="types"
        @on-update="onUpdateDownPay"
        @on-delete="onDeleteDownPay"
      />
    </CTableBody>

    <CTableBody v-else>
      <CTableRow>
        <CTableDataCell colspan="9" class="text-center p-5 text-danger">
          등록된 데이터가 없습니다.
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
