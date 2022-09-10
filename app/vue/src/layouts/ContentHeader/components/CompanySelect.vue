<script lang="ts" setup>
import { ref, computed, nextTick, onBeforeMount } from 'vue'
import { useCompany } from '@/store/pinia/company'

const emit = defineEmits(['com-select'])

const currentCompany = ref()

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const comSelectList = computed(() => companyStore.comSelect)

const comSelect = (event: Event) =>
  nextTick(() => emit('com-select', (event.target as HTMLSelectElement).value))

onBeforeMount(() => {
  companyStore.fetchCompanyList()
  currentCompany.value = initComId.value
  companyStore.fetchCompany(currentCompany.value)
})
</script>

<template>
  <CRow>
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="currentCompany" @change="comSelect">
        <option value="">회사선택</option>
        <option v-for="c in comSelectList" :key="c.value" :value="c.value">
          {{ c.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
