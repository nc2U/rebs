<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import DownPay from '@/views/projects/DownPay/components/DownPay.vue'
import { headerSecondary } from '@/utils/cssMixins'

defineProps({
  orders: { type: Object, default: null },
  types: { type: Object, default: null },
})
const emit = defineEmits(['on-update', 'on-delete'])

const store = useStore()
const downPayList = computed(() => store.state.payment.downPayList)

const onUpdateDownPay = (payload: any) => emit('on-update', payload)
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
    <CTableHead :color="headerSecondary" class="text-center">
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
