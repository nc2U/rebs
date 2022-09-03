<script lang="ts" setup>
import { ref } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteContractForm from './SiteContractForm.vue'

const props = defineProps({
  contract: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
const isDoneText = (bool: boolean) => (bool ? '완료' : '-')
const isDoneClass = (bool: boolean) => (bool ? 'bg-success' : '')
</script>

<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>{{ contract.owner_desc.own_sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ contract.owner_desc.owner }}</CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.contract_area, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat(contract.contract_area * 0.3025, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_price) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.down_pay1) }}
    </CTableDataCell>
    <CTableDataCell :class="isDoneClass(contract.down_pay1_is_paid)">
      {{ isDoneText(contract.down_pay1_is_paid) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.down_pay2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.inter_pay1) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.inter_pay2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.remain_pay) }}
    </CTableDataCell>
    <CTableDataCell :class="isDoneClass(contract.remain_pay_is_paid)">
      {{ isDoneText(contract.remain_pay_is_paid) }}
    </CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 매입 계약 등록
    </template>
    <template #default>
      <SiteContractForm
        :contract="contract"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
