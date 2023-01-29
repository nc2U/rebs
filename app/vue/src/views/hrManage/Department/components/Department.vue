<script lang="ts" setup="">
import DepartmentForm from './DepartmentForm.vue'

defineProps({
  department: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <CTableRow v-if="department" class="text-center">
    <CTableDataCell>{{ department.pk }}</CTableDataCell>
    <CTableDataCell>{{ department.upper_depart }}</CTableDataCell>
    <CTableDataCell>{{ department.name }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ department.task }}</CTableDataCell>
  </CTableRow>

  <!--  <FormModal ref="updateFormModal" size="lg">-->
  <!--    <template #header>-->
  <!--      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />-->
  <!--      사업 부지 등록-->
  <!--    </template>-->
  <!--    <template #default>-->
  <!--      <DepartmentForm-->
  <!--        :site="site"-->
  <!--        @multi-submit="multiSubmit"-->
  <!--        @on-delete="onDelete"-->
  <!--        @close="updateFormModal.close()"-->
  <!--      />-->
  <!--    </template>-->
  <!--  </FormModal>-->
</template>
