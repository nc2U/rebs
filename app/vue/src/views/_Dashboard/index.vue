<script lang="ts" setup>
import TodoListApp from '@/components/TodoListApp/index.vue'
import MainCarousel from './components/MainCarousel.vue'
import WidgetsStatsA from './components/widgets/WidgetsStatsTypeA.vue'
import WidgetsStatsB from './components/widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/widgets/WidgetsStatsTypeD.vue'
</script>

<template>
  <CContainer fluid>
    aa
    <CRow>
      <CCol xl="11" xxl="10">
        <MainCarousel />
      </CCol>
      <CCol xl="11" xxl="10">
        <CRow>
          <CCol lg="6">
            <TodoListApp />
          </CCol>
          <CCol lg="6">
            <WidgetsStatsA />
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <WidgetsStatsB />
    <WidgetsStatsD />
    <WidgetsStatsC />
  </CContainer>
</template>
