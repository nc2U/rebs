<script setup lang="ts">
import { computed, type ComputedRef, inject, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import { useRoute } from 'vue-router'
import type { Company } from '@/store/types/settings'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import SearchList from '@/views/_Work/Manages/Projects/components/SearchList.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const route = useRoute()

const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ route.name }}</h5>
        </CCol>
      </CRow>

      <SearchList />

      <CRow class="mb-3">
        <CCol> Gantt Chart</CCol>
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
