<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'

const emit = defineEmits(['aside-visible'])

const route = useRoute()

const capitalize = (str: string) => `${str.charAt(0).toUpperCase()}${str.slice(1)}`

const wikiTitle = computed(() =>
  route.params.title ? capitalize(route.params.title as string) : 'Wiki',
)

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>{{ wikiTitle }}</h5>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CFormTextarea> #{{ wikiTitle }}</CFormTextarea>
    </CCol>
  </CRow>

  <CRow class="mt-2">
    <CCol>
      <CButton color="primary">저장</CButton>
      <CButton color="light">취소</CButton>
    </CCol>
  </CRow>
</template>
