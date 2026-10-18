<script lang="ts" setup>
import { computed, ref } from 'vue'
import { usePerms } from '@/composables/usePerms.ts'
import { type Duty } from '@/store/types/company.ts'
import FormModal from '@/components/Modals/FormModal.vue'
import DutyForm from './DutyForm.vue'

defineProps<{
  duty: Duty
}>()

const emit = defineEmits<{
  (e: 'multi-submit', payload: Duty): void
  (e: 'on-delete', pk: number): void
}>()

const { canGlobal, PERM } = usePerms()
const canHrWorkManage = computed(
  () => canGlobal(PERM.HQ_HR_WORK_CREATE) || canGlobal(PERM.HQ_HR_WORK_UPDATE),
)

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: Duty) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTableRow v-if="duty" class="text-center">
    <CTableDataCell>{{ duty.pk }}</CTableDataCell>
    <CTableDataCell>{{ duty.code }}</CTableDataCell>
    <CTableDataCell>{{ duty.name }}</CTableDataCell>
    <CTableDataCell class="text-start">{{ duty.desc }}</CTableDataCell>
    <CTableDataCell v-if="canHrWorkManage">
      <v-btn color="info" variant="flat" size="x-small" @click="showDetail">확인</v-btn>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직책 정보 수정</template>
    <template #default>
      <DutyForm
        :duty="duty"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
