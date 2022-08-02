<script lang="ts" setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useStore } from 'vuex'

const com = ref()

const props = defineProps({ company: { type: Object, default: null } })

const store = useStore()
const comSelectList = computed(() => store.getters['settings/comSelect'])
const initComId = computed(() => store.getters['accounts/initComId'])

const fetchCompanyList = () => store.dispatch('settings/fetchCompanyList')
const emit = defineEmits(['com-select'])
const selectCom = () => {
  nextTick(() => {
    emit('com-select', com.value)
  })
}

onMounted(() => {
  com.value = initComId.value
  fetchCompanyList()
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
