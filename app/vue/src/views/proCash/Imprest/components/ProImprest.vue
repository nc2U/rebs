<script lang="ts" setup>
import { ref, computed } from 'vue'
import { numFormat, cutString } from '@/utils/baseMixins'
import { ProjectCashBook } from '@/store/types/proCash'
import FormModal from '@/components/Modals/FormModal.vue'
import ProImprestForm from '@/views/proCash/Imprest/components/ProImprestForm.vue'

const props = defineProps({
  imprest: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const sortClass = computed(
  () => ['', 'text-primary', 'text-danger', 'text-info'][props.imprest.sort],
)

const rowColor = computed(() => {
  let color = ''
  color =
    props.imprest.contract && props.imprest.project_account_d2 <= '2'
      ? 'info'
      : color
  color = props.imprest.is_separate ? 'dark' : color
  color = props.imprest.separated ? 'primary' : color
  return color
})

const showDetail = () => updateFormModal.value.callModal()

const multiSubmit = (payload: {
  formData: ProjectCashBook
  sepData: ProjectCashBook | null
}) => emit('multi-submit', payload)

const onDelete = (payload: { project: number; pk: number }) =>
  emit('on-delete', payload)
</script>

<template>
  <CTableRow
    v-if="imprest"
    class="text-center"
    :color="rowColor"
    :style="imprest.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ imprest.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ imprest.sort_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ imprest.project_account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.project_account_d2_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.trader, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.bank_account_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(imprest.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(imprest.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ imprest.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      운영비(전도금) 거래 건별 관리
    </template>
    <template #default>
      <ProImprestForm
        :imprest="imprest"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
