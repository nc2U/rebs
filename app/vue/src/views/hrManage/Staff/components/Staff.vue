<script lang="ts" setup="">
import StaffForm from './StaffForm.vue'

defineProps({
  staff: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <CTableRow v-if="staff" class="text-center">
    <CTableDataCell>{{ staff.pk }}</CTableDataCell>
    <CTableDataCell>{{ staff.department }}</CTableDataCell>
    <CTableDataCell>{{ staff.rank }}</CTableDataCell>
    <CTableDataCell>{{ staff.name }}</CTableDataCell>
    <CTableDataCell>{{ staff.birth_date }}</CTableDataCell>
    <CTableDataCell>{{ staff.gender_desc }}</CTableDataCell>
    <CTableDataCell>{{ staff.entered_date }}</CTableDataCell>
    <CTableDataCell>{{ staff.personal_phone }}</CTableDataCell>
    <CTableDataCell>{{ staff.email }}</CTableDataCell>
    <CTableDataCell>{{ staff.status_desc }}</CTableDataCell>
  </CTableRow>

  <!--  <FormModal ref="updateFormModal" size="lg">-->
  <!--    <template #header>-->
  <!--      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />-->
  <!--      사업 부지 등록-->
  <!--    </template>-->
  <!--    <template #default>-->
  <!--      <StaffForm-->
  <!--        :site="site"-->
  <!--        @multi-submit="multiSubmit"-->
  <!--        @on-delete="onDelete"-->
  <!--        @close="updateFormModal.close()"-->
  <!--      />-->
  <!--    </template>-->
  <!--  </FormModal>-->
</template>
