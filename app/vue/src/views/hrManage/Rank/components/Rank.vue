<script lang="ts" setup="">
// import { ref } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import StaffForm from './RankForm.vue'

defineProps({
  rank: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['show-detail'])

const showDetail = () => emit('show-detail')
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
