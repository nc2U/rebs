<script lang="ts" setup>
import { ref, watch } from 'vue'
import { downloadFile } from '@/utils/helper.ts'
import { AlertSecondary } from '@/utils/cssMixins.ts'
import AlertModal from '@/components/Modals/AlertModal.vue'

interface PrintData {
  is_bill_issue: boolean
  project: number | null
  pub_date: string
}

interface Props {
  printData?: PrintData | null
  contracts?: number[]
}

const props = withDefaults(defineProps<Props>(), {
  printData: null,
  contracts: () => [],
})

const refAlertModal = ref<InstanceType<typeof AlertModal> | null>(null)

const noPrice = ref(localStorage.getItem('noPrice') === 'true')

watch(noPrice, newVal => {
  localStorage.setItem('noPrice', String(newVal))
})

const noLate = ref(localStorage.getItem('noLate') === 'true')

watch(noLate, newVal => {
  localStorage.setItem('noLate', String(newVal))
})

const printBill = () => {
  if (!props.printData?.is_bill_issue) {
    refAlertModal.value?.callModal('', '고지서 관련 기본 설정 데이터를 입력하여 주십시요.')
  } else {
    if (props.contracts?.length === 0) {
      refAlertModal.value?.callModal('', '다운로드(출력)할 계약 건을 선택하여 주십시요.')
    } else {
      const { project, pub_date } = props.printData
      const seq = props.contracts?.join('-')
      const url = '/pdf/bill/'
      const np = noPrice.value ? '1' : ''
      const nl = noLate.value ? '1' : ''
      const lastUrl = `${url}?project=${project}&date=${pub_date}&seq=${seq}&np=${np}&nl=${nl}`
      downloadFile(lastUrl, `대금납부_고지서(${props.contracts.length}건).pdf`)
    }
  }
}
</script>

<template>
  <CAlert :color="AlertSecondary" class="pb-2">
    <CRow class="p-0 m-0">
      <CCol sm="6">
        <v-btn color="primary" variant="flat" :disabled="!contracts.length" @click="printBill">
          선택 건별 고지서 내려받기
        </v-btn>
      </CCol>
      <CCol sm="6" class="d-flex justify-content-end align-items-center">
        <v-checkbox-btn
          v-model="noPrice"
          color="success"
          label="가격정보 미표시"
          inline
          class="flex-grow-0 me-3"
        />
        <v-checkbox-btn
          v-model="noLate"
          color="success"
          label="연체정보 미표시"
          inline
          class="flex-grow-0"
        />
      </CCol>
    </CRow>
  </CAlert>

  <AlertModal ref="refAlertModal" />
</template>
