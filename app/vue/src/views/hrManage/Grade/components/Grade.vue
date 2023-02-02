<script lang="ts" setup="">
import { computed, ref } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { Grade } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './GradeForm.vue'

const props = defineProps({
  grade: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const comStore = useCompany()
const pkPositions = computed(() => comStore.getPkPositions)

const positions = computed(() => {
  const ids = props.grade.positions
  return pkPositions.value
    .filter(p => ids.includes(p.value))
    .map(p => p.label)
    .join(', ')
})

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Grade) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="grade" class="text-center">
    <CTableDataCell>{{ grade.pk }}</CTableDataCell>
    <CTableDataCell>{{ grade.name }}</CTableDataCell>
    <CTableDataCell>{{ grade.promotion_period }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ positions }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ grade.criteria_new }}</CTableDataCell>
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
