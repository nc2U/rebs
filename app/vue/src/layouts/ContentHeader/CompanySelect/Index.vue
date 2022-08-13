<script lang="ts" setup>
import { ref, computed, nextTick, onBeforeMount } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { useAccount } from '@/store/pinia/account'

const com = ref()
const companyStore = useCompany()
const accountStore = useAccount()

const props = defineProps({ company: { type: Object, default: null } })

const comSelectList = computed(() => companyStore.comSelect)
const initComId = computed(() => accountStore.initComId)

const emit = defineEmits(['com-select'])
const selectCom = () => {
  nextTick(() => {
    emit('com-select', com.value)
  })
}

onBeforeMount(() => {
  com.value = initComId.value
  companyStore.fetchCompanyList()
})
</script>

<template>
  <CRow>
    <CFormLabel class="col-lg-1 col-form-label text-body">회사명</CFormLabel>
    <CCol md="6" lg="3">
      <CFormSelect v-model="com" @change="selectCom">
        <option value="">회사선택</option>
        <option v-for="c in comSelectList" :key="c.value" :value="c.value">
          {{ c.text }}
        </option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
