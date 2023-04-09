<script lang="ts" setup>
import { ref, computed, nextTick, onBeforeMount, watch } from 'vue'
import { useCompany } from '@/store/pinia/company'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['com-select'])

const currentCompany = ref()

const companyStore = useCompany()
const company = computed(() => companyStore.company?.pk)
const initComId = computed(() => companyStore.initComId)
const comSelectList = computed(() => companyStore.comSelect)

watch(company, val => (currentCompany.value = val))

const comSelect = () => nextTick(() => emit('com-select', currentCompany.value))

onBeforeMount(() => {
  companyStore.fetchCompanyList()
  currentCompany.value = company.value ? company.value : initComId.value
  companyStore.fetchCompany(currentCompany.value)
})
</script>

<template>
  <CRow class="m-0 align-items-center">
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <Multiselect
        v-model="currentCompany"
        :options="comSelectList"
        placeholder="회사선택"
        autocomplete="label"
        :classes="{ search: 'form-control multiselect-search' }"
        :add-option-on="['enter' | 'tab']"
        searchable
        @change="comSelect"
      />
    </CCol>
    <CCol v-if="comSelectList.length === 0" class="pl-0 align-middle">
      <v-icon icon="mdi mdi-plus-thick" color="primary" />
    </CCol>
  </CRow>
</template>
