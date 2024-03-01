<script setup lang="ts">
import { computed, ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import { useWork } from '@/store/pinia/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import NoData from '@/views/_Work/components/NoData.vue'

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const iProjectList = computed(() => workStore.issueProjectList)
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>
      </CRow>

      <SearchList />

      <NoData v-if="!iProjectList.length" />

      <CRow v-else>
        <CCol></CCol>
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
