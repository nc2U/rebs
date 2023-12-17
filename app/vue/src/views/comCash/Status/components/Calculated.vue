<script lang="ts" setup>
import { ref } from 'vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'

defineProps({ isCalculated: { type: Boolean, default: false } })
const emit = defineEmits(['to-calculate'])

const refConfirmModal = ref()

const toCalculated = () => refConfirmModal.value.callModal()

const modalAction = () => {
  emit('to-calculate')
  refConfirmModal.value.close()
}
</script>

<template>
  <CAlert :color="isCalculated ? 'success' : 'warning'" class="text-right">
    <v-btn v-if="isCalculated" size="x-large" disabled="">잔고 확인 완료</v-btn>
    <v-btn v-else color="warning" size="x-large" @click="toCalculated">금일 잔고 확인</v-btn>
  </CAlert>

  <ConfirmModal ref="refConfirmModal">
    <template #header> 알림</template>
    <template #default>
      계좌별 잔고 데이터가 실제 계좌 잔고와 일치 하는 경우 확인을 클릭 하십시요. 확인을 클릭한 이후
      현재 등록된 최종 거래일자 이전의 거래를 수정 및 삭제할 수 없습니다.
    </template>
    <template #footer>
      <CButton color="warning" @click="modalAction">확인</CButton>
    </template>
  </ConfirmModal>
</template>
