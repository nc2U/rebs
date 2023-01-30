<script lang="ts" setup="">
import { ref, computed } from 'vue'
import { Department } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import DepartmentForm from './DepartmentForm.vue'

const props = defineProps({
  department: {
    type: Object,
    required: true,
  },
  departs: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const upper_depart = computed(() => {
  const ud = props.department.upper_depart
  const departs = props.departs as { pk: number; name: string }[]
  return !!ud
    ? departs.filter((d: { pk: number; name: string }) => d.pk === ud)[0].name
    : ''
})

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Department) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow v-if="department" class="text-center">
    <CTableDataCell>{{ department.pk }}</CTableDataCell>
    <CTableDataCell>{{ upper_depart }}</CTableDataCell>
    <CTableDataCell>{{ department.name }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ department.task }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>부서 정보 등록</template>
    <template #default>
      <DepartmentForm
        :department="department"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
