<template>
  <CContainer>
    <MainCarousel />
    <CRow>
      <CCol lg="6">
        <!--        <TodoListApp />-->
      </CCol>
      <CCol lg="6">
        <WidgetsStatsA />
      </CCol>
    </CRow>
    <WidgetsStatsB />
    <WidgetsStatsD />
    <WidgetsStatsC />
  </CContainer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import MainCarousel from './components/MainCarousel.vue'
// import TodoListApp from './components/TodoListApp/index.vue'
import WidgetsStatsA from './components/widgets/WidgetsStatsTypeA.vue'
import WidgetsStatsB from './components/widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/widgets/WidgetsStatsTypeD.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    MainCarousel,
    // TodoListApp,
    WidgetsStatsA,
    WidgetsStatsB,
    WidgetsStatsC,
    WidgetsStatsD,
  },
})
</script>
