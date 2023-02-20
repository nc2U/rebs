<script lang="ts" setup>
import { ref, watch, nextTick } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['set-date', 'set-sort'])

const date = ref(new Date())
const sort = ref('0')

watch(date, val => {
  if (!val) date.value = new Date()
  setDate()
})
const setDate = () => emit('set-date', dateFormat(date.value))
const setSort = () => nextTick(() => emit('set-sort', sort.value))

const sortOptions = [
  { value: '0', label: '전체 집계' },
  { value: '1', label: '계약건 집계' },
  { value: '2', label: '미계약건 집계' },
]
</script>

<template>
  <CCallout color="success">
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label">기준일자</CFormLabel>
      <CCol md="6" lg="3">
        <DatePicker v-model="date" @keydown.enter="setDate" />
      </CCol>

      <CFormLabel class="col-lg-1 col-form-label">구분</CFormLabel>
      <CCol md="6" lg="3">
        <Multiselect v-model="sort" :options="sortOptions" @change="setSort" />
      </CCol>
    </CRow>
  </CCallout>
</template>
