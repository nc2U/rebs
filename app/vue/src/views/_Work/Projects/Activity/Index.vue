<script setup lang="ts">
import { computed, type ComputedRef, inject, ref } from 'vue'
import { navMenu } from '@/views/_Work/_menu/headermixin1'
import type { Company } from '@/store/types/settings'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol>2024/02/21부터 2024/03/01까지</CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CAlert color="warning">표시할 데이터가 없습니다.</CAlert>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <CButtonGroup role="group">
            <CButton color="primary" variant="outline" size="sm">« 뒤로</CButton>
            <CButton color="primary" variant="outline" size="sm">다음 »</CButton>
          </CButtonGroup>
        </CCol>
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
