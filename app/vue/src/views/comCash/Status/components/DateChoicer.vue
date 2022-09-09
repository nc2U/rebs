<script lang="ts" setup>
import { ref, watch } from 'vue'
import { dateFormat } from '@/utils/baseMixins'
import DatePicker from '@/components/DatePicker/index.vue'

const emit = defineEmits(['set-date'])

const date = ref(new Date())
watch(date, val => {
  if (!val) date.value = new Date()
  setDate()
})
const setDate = () => emit('set-date', dateFormat(date.value))
</script>

<template>
  <CCallout color="primary">
    <CRow>
      <CFormLabel class="col-lg-1 col-form-label">기준일자</CFormLabel>
      <CCol md="6" lg="3">
        <DatePicker v-model="date" @keydown.enter="setDate" />
      </CCol>
    </CRow>
  </CCallout>
</template>
