<script lang="ts" setup>
import { computed } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { PayOrder as po } from '@/store/types/payment'
import { headerSecondary } from '@/utils/cssMixins'
import PayOrder from '@/views/projects/PayOrder/components/PayOrder.vue'

const emit = defineEmits(['on-update', 'on-delete'])

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)

const onUpdatePayOrder = (payload: po) => emit('on-update', payload)
const onDeletePayOrder = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="11%" />
      <col width="12%" />
    </colgroup>
    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>종류</CTableHeaderCell>
        <CTableHeaderCell>납입회차 코드</CTableHeaderCell>
        <CTableHeaderCell>납부순서</CTableHeaderCell>
        <CTableHeaderCell>PM용역비 여부</CTableHeaderCell>
        <CTableHeaderCell>납부회차명</CTableHeaderCell>
        <CTableHeaderCell>회차 별칭</CTableHeaderCell>
        <CTableHeaderCell>납부기한일</CTableHeaderCell>
        <CTableHeaderCell>납부유예일</CTableHeaderCell>
        <CTableHeaderCell>비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
    <CTableBody v-if="payOrderList.length > 0">
      <PayOrder
        v-for="payOrder in payOrderList"
        :key="payOrder.pk"
        :pay-order="payOrder"
        @on-update="onUpdatePayOrder"
        @on-delete="onDeletePayOrder"
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
