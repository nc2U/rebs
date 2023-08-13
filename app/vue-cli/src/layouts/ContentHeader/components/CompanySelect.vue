<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useCompany } from '@/store/pinia/company'
import Multiselect from '@vueform/multiselect'

const emit = defineEmits(['com-select'])

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)
const comSelectList = computed(() => comStore.comSelect)

const comSelect = (com: number) => emit('com-select', com)
const comClear = () => emit('com-select', null)

onBeforeMount(() => {
  comStore.fetchCompanyList()
  comStore.fetchCompany(company.value || comStore.initComId)
})
</script>

<template>
  <CRow class="m-0 align-items-center">
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <Multiselect
        :value="company"
        :options="comSelectList"
        placeholder="회사선택"
        autocomplete="label"
        :classes="{ search: 'form-control multiselect-search' }"
        :add-option-on="['enter', 'tab']"
        searchable
        @select="comSelect"
        @clear="comClear"
      />
    </CCol>
    <CCol v-if="comSelectList.length === 0" class="pl-0 align-middle">
      <v-icon
        icon="mdi mdi-plus-thick"
        color="primary"
        @click="$router.push({ name: '회사 정보 관리' })"
      />
    </CCol>
  </CRow>
</template>
