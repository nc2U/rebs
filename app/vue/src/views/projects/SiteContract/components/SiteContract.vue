<script lang="ts" setup>
import { type PropType, ref } from 'vue'
import { type SiteContract } from '@/store/types/project'
import { numFormat } from '@/utils/baseMixins'
import { write_project_site } from '@/utils/pageAuth'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteContractForm from './SiteContractForm.vue'

defineProps({
  contract: { type: Object as PropType<SiteContract>, required: true },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: SiteContract) => emit('multi-submit', payload)
const onDelete = (payload: { pk: number; project: number }) => emit('on-delete', payload)
const isDoneText = (bool: boolean) => (bool ? '완료' : '-')
const isDoneClass = (bool: boolean) => (bool ? 'bg-success' : '')
</script>

<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>{{ contract.owner_desc?.own_sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ contract.owner_desc?.owner }}</CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.contract_area as number, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat((contract.contract_area as number) * 0.3025, 2) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_price as number) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.down_pay1 as number) }}
    </CTableDataCell>
    <CTableDataCell :class="isDoneClass(contract.down_pay1_is_paid)">
      {{ isDoneText(contract.down_pay1_is_paid) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.down_pay2 as number) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.inter_pay1 as number) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.remain_pay as number) }}
    </CTableDataCell>
    <CTableDataCell :class="isDoneClass(contract.remain_pay_is_paid)">
      {{ isDoneText(contract.remain_pay_is_paid) }}
    </CTableDataCell>
    <CTableDataCell v-if="write_project_site">
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>부지 매입 계약 등록</template>
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
