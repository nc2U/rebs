<script lang="ts" setup="">
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './StaffForm.vue'

defineProps({
  staff: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['show-detail'])

const showDetail = () => emit('show-detail')
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
    <template #header>사업 부지 등록</template>
    <template #default>
      <StaffForm
        :site="site"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
