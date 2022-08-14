<script lang="ts" setup>
import { ref, computed, nextTick, onBeforeMount } from 'vue'
import { useCompany } from '@/store/pinia/company'

const com = ref()
const companyStore = useCompany()

defineProps({ company: { type: Object, default: null } })

const initComId = computed(() => companyStore.initComId)
const comSelectList = computed(() => companyStore.comSelect)

const emit = defineEmits(['com-select'])
const comSelect = (event: any) => {
  nextTick(() => {
    emit('com-select', event.target.value)
  })
}

onBeforeMount(() => {
  com.value = initComId.value
  companyStore.fetchCompany(com.value)
  companyStore.fetchCompanyList()
})
</script>

<template>
  <CRow>
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="com" @change="comSelect">
        <option value="">회사선택</option>
        <option v-for="c in comSelectList" :key="c.value" :value="c.value">
          {{ c.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
