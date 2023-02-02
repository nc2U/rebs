<script lang="ts" setup="">
import { ref } from 'vue'
import { Duty } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './DutyForm.vue'

defineProps({
  duty: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Duty) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="duty" class="text-center">
    <CTableDataCell>{{ duty.pk }}</CTableDataCell>
    <CTableDataCell>{{ duty.name }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ duty.title }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직급 정보 등록</template>
    <template #default>
      <StaffForm
        :duty="duty"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
