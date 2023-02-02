<script lang="ts" setup="">
import { ref } from 'vue'
import { Position } from '@/store/types/company'
import FormModal from '@/components/Modals/FormModal.vue'
import PositionForm from './PositionForm.vue'

defineProps({
  position: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Position) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="position" class="text-center">
    <CTableDataCell>{{ position.pk }}</CTableDataCell>
    <CTableDataCell>{{ position.name }}</CTableDataCell>
    <CTableDataCell>{{ position.desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직급 정보 등록</template>
    <template #default>
      <PositionForm
        :position="position"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
