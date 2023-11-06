<script lang="ts" setup>
import MainCarousel from './components/MainCarousel.vue'
import WiseWord from '@/views/_Dashboard/components/WiseWord.vue'
import WidgetsStatsB from './components/widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/widgets/WidgetsStatsTypeD.vue'
</script>

<template>
  <CContainer fluid>
    <CRow>
      <CCol xl="11" xxl="10">
        <MainCarousel />
      </CCol>
    </CRow>
    <CRow>
      <CCol xl="11" xxl="10">
        <CRow>
          <CCol lg="12">
            <WiseWord />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol>
        <WidgetsStatsB />
      </CCol>
    </CRow>
    <CRow>
      <CCol>
        <WidgetsStatsD />
      </CCol>
    </CRow>
    <CRow>
      <CCol>
        <WidgetsStatsC />
      </CCol>
    </CRow>
  </CContainer>
</template>
