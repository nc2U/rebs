<script setup lang="ts">
import { ref } from 'vue'
import { pageTitle, navMenu } from '@/views/_Work/_menu/headermixin3'
import { useRoute } from 'vue-router'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'

const route = useRoute()

const cBody = ref()
const sideNavCAll = () => cBody.value.toggle()
</script>

<template>
  <Header :page-title="pageTitle" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ route.name }}</h5>
        </CCol>
      </CRow>
    </template>

    <template v-slot:aside></template>
  </ContentBody>
</template>
