<template>
  <CContainer fluid>
    <CRow>
      <CCol xxl="9">
        <MainCarousel />
      </CCol>
      <CCol xxl="9">
        <CRow>
          <CCol md="6">
            <TodoListApp />
          </CCol>
          <CCol md="6">
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

<script lang="ts">
import { defineComponent } from 'vue'
import TodoListApp from '@/components/TodoListApp/index.vue'
import MainCarousel from './components/MainCarousel.vue'
import WidgetsStatsA from './components/widgets/WidgetsStatsTypeA.vue'
import WidgetsStatsB from './components/widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/widgets/WidgetsStatsTypeD.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    MainCarousel,
    TodoListApp,
    WidgetsStatsA,
    WidgetsStatsB,
    WidgetsStatsC,
    WidgetsStatsD,
  },
})
</script>
