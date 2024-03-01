<script lang="ts" setup="">
import { onBeforeMount, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const search = ref('')

const [route, router] = [useRoute(), useRouter()]

const goSearch = () => router.push({ name: '전체검색', query: { scope: '', q: search.value } })

onBeforeMount(() => {
  if (route?.query.q) search.value = route.query.q as string
})
</script>

<template>
  <CRow>
    <CCol class="p-1">
      <CInputGroup size="" class="mb-3">
        <CInputGroupText id="inputGroup-sizing-sm" @click="goSearch">검색</CInputGroupText>
        <CFormInput v-model="search" @keydown.enter="goSearch" @focusin="search = ''" />
      </CInputGroup>
    </CCol>
    <CCol class="p-1">
      <CFormSelect size="" class="mb-3">
        <option>프로젝트 바로가기</option>
      </CFormSelect>
    </CCol>
  </CRow>
</template>
