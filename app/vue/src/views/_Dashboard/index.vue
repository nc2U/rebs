<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import { useStore } from '@/store'
import MainCarousel from './components/MainCarousel.vue'
import WiseWord from '@/views/_Dashboard/components/WiseWord.vue'
import WidgetsStatsA from './components/widgets/WidgetsStatsTypeA.vue'
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

<style scoped lang="scss">
.animated-title {
  font-family: 'Raleway', Sans-serif, serif;
  position: relative;
  width: 100%;
  max-width: 100%;
  height: auto;
  padding: 100px 0;
  overflow-x: hidden;
  overflow-y: hidden;
}

.animated-title .track {
  position: absolute;
  white-space: nowrap;
  will-change: transform;
  animation: marquee 60s linear infinite;
}

@keyframes marquee {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

@media (hover: hover) and (min-width: 700px) {
  .animated-title .content {
    -webkit-transform: translateY(calc(100% - 8rem));
    transform: translateY(calc(100% - 8rem));
  }
}
</style>
