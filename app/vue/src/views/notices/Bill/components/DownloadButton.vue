<script lang="ts" setup>
import { ref } from 'vue'
import { AlertLight } from '@/utils/cssMixins'
import AlertModal from '@/components/Modals/AlertModal.vue'

const props = defineProps({
  printData: { type: Object, default: null },
  contractors: { type: Array, default: () => [] },
})

const alertModal = ref()

const printBill = () => {
  if (!props.printData.is_bill_issue) {
    alertModal.value.callModal(
      '',
      '고지서 관련 기본 설정 데이터를 입력하여 주십시요.',
    )
  } else {
    if (props.contractors?.length === 0) {
      alertModal.value.callModal(
        '',
        '다운로드(출력)할 계약 건을 선택하여 주십시요.',
      )
    } else {
      const project = props.printData.project
      const pub_date = props.printData.pub_date
      const seq = props.contractors.join('-')
      const url = 'rebs/pdf-bill/'
      location.href = `${url}?project=${project}&date=${pub_date}&seq=${seq}`
    }
  }
}
</script>

<template>
  <CAlert :color="AlertLight" variant="solid">
    <CButton color="primary" :disabled="!contractors.length" @click="printBill">
      선택 건별 고지서 내려받기
    </CButton>
  </CAlert>

  <AlertModal ref="alertModal" />
</template>
