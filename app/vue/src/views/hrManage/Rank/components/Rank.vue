<script lang="ts" setup="">
import { ref } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './RankForm.vue'

defineProps({
  rank: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['multi-submit', 'on-delete'])

const updateFormModal = ref()

const showDetail = () => updateFormModal.value.callModal()
const multiSubmit = (payload: any) => emit('multi-submit', payload)
const onDelete = (payload: any) => emit('on-delete', payload)
</script>

<template>
  <CTableRow v-if="rank" class="text-center">
    <CTableDataCell>{{ rank.pk }}</CTableDataCell>
    <CTableDataCell>{{ rank.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ rank.rank }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ rank.title }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ rank.description }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>직급 정보 등록</template>
    <template #default>
      <StaffForm
        :rank="rank"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
