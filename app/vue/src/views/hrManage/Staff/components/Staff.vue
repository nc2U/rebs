<script lang="ts" setup="">
import { ref } from 'vue'
import StaffForm from './StaffForm.vue'

const msg = ref('직원')
</script>

<template>
  <CTableRow>
    <CTableDataCell>1</CTableDataCell>
    <CTableDataCell>a</CTableDataCell>
    <CTableDataCell>b</CTableDataCell>
    <CTableDataCell>c</CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      사업 부지 등록
    </template>
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
