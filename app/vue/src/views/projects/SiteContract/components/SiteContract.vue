<script lang="ts" setup>
import { ref } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import FormModal from '@/components/Modals/FormModal.vue'
import SiteContractForm from './SiteContractForm.vue'

const props = defineProps({
  site: {
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
  <!--  <CTableRow-->
  <!--    v-if="site"-->
  <!--    class="text-center"-->
  <!--  >-->
  <CTableRow class="text-center">
    <CTableDataCell>국공유지</CTableDataCell>
    <CTableDataCell>홍길동</CTableDataCell>
    <CTableDataCell>2022-09-01</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(1000000) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="warning">
      {{ numFormat(300000) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(20000000000) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(10000000) }}
    </CTableDataCell>
    <CTableDataCell>완료</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(10000000) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(160000000) }}
    </CTableDataCell>
    <CTableDataCell>완료</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" size="sm" @click="showDetail">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="updateFormModal" size="lg">
    <template #header>
      <v-icon icon="mdi-briefcase-plus" size="small" color="dark" />
      부지 매입 계약 등록
    </template>
    <template #default>
      <SiteContractForm
        :site="site"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="updateFormModal.close()"
      />
    </template>
  </FormModal>
</template>
