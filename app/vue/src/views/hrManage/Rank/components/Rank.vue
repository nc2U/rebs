<script lang="ts" setup="">
// import { ref } from 'vue'
// import StaffForm from './RankForm.vue'

defineProps({
  rank: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <CTableRow v-if="rank" class="text-center">
    <CTableDataCell>{{ rank.pk }}</CTableDataCell>
    <CTableDataCell>{{ rank.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ rank.rank }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ rank.title }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ rank.description }}</CTableDataCell>
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
