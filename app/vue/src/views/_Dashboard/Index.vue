<script lang="ts" setup>
import MainCarousel from './components/MainCarousel.vue'
import WiseWord from '@/views/_Dashboard/components/WiseWord.vue'
import NoticeBoard from './components/NoticeBoard/Index.vue'
import WidgetsStatsB from './components/Widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/Widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/Widgets/WidgetsStatsTypeD.vue'
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
      <CCol xl="6">
        <NoticeBoard />
      </CCol>
      <CCol xl="6">
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
