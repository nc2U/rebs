<script lang="ts" setup="">
import { ref } from 'vue'
import { Staff } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './StaffForm.vue'

defineProps({
  staff: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Staff) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="staff" class="text-center">
    <CTableDataCell>{{ staff.pk }}</CTableDataCell>
    <CTableDataCell>{{ staff.department }}</CTableDataCell>
    <CTableDataCell>{{ staff.rank }}</CTableDataCell>
    <CTableDataCell>{{ staff.name }}</CTableDataCell>
    <CTableDataCell>{{ staff.entered_date }}</CTableDataCell>
    <CTableDataCell>{{ staff.personal_phone }}</CTableDataCell>
    <CTableDataCell>{{ staff.email }}</CTableDataCell>
    <CTableDataCell>{{ staff.status_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직원 정보 등록</template>
    <template #default>
      <StaffForm
        :staff="staff"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
