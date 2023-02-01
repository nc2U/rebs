<script lang="ts" setup="">
import { ref } from 'vue'
import { Grade } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './GradeForm.vue'

defineProps({
  rank: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Grade) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="grade" class="text-center">
    <CTableDataCell>{{ grade.pk }}</CTableDataCell>
    <CTableDataCell>{{ grade.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ grade.grade }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ grade.title }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ grade.description }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직급 정보 등록</template>
    <template #default>
      <StaffForm
        :grade="grade"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
