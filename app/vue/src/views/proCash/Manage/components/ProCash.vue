<script lang="ts" setup>
import { ref, computed } from 'vue'
import { numFormat, cutString } from '@/utils/baseMixins'
import { ProjectCashBook } from '@/store/types/proCash'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'

const props = defineProps({
  proCash: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const sortClass = computed(() => {
  const cls = ['', 'text-primary', 'text-danger', 'text-info']
  return cls[props.proCash.sort]
})

const rowColor = computed(() => {
  let color = ''
  color =
    props.proCash.contract && props.proCash.project_account_d2 <= '2'
      ? 'info'
      : color
  color = props.proCash.is_separate ? 'primary' : color
  color = props.proCash.separated ? 'secondary' : color
  return color
})

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: ProjectCashBook) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow
    v-if="proCash"
    class="text-center"
    :color="rowColor"
    :style="proCash.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ proCash.sort_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ proCash.project_account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.project_account_d2_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.trader, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.bank_account_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(proCash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(proCash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 관리
    </template>
    <template #default>
      <ProCashForm
        :pro-cash="proCash"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
