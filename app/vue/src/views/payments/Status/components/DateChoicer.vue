<script lang="ts" setup>
import { ref, watch } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['set-date'])

const date = ref(new Date())

watch(date, val => {
  if (!val) date.value = new Date()
  setDate()
})
const setDate = () => emit('set-date', dateFormat(date.value))

const sort = ref('0')
const sortOptions = [
  { value: '0', label: '전체 현황' },
  { value: '1', label: '계약 현황' },
  { value: '2', label: '미계약 현황' },
]
</script>

<template>
  <CCallout color="success">
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label">기준일자</CFormLabel>
      <CCol md="6" lg="3">
        <DatePicker v-model="date" @keydown.enter="setDate" />
      </CCol>

      <CFormLabel class="col-lg-1 col-form-label">현황구분</CFormLabel>
      <CCol md="6" lg="3">
        <Multiselect v-model="sort" :options="sortOptions" />
      </CCol>
    </CRow>
  </CCallout>
</template>
