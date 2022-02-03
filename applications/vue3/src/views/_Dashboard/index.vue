<template>
  <CContainer>
    <MainCarousel />
    <CRow>
      <CCol xs="6">
        <TodoList />
        <!--        <TodoMVC />-->
      </CCol>
      <CCol xs="6">
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
import TodoList from './components/TodoList/index.vue'
// import TodoMVC from '@/views/_Dashboard/components/TodoMVC.vue'
import WidgetsStatsA from './components/widgets/WidgetsStatsTypeA.vue'
import WidgetsStatsB from './components/widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/widgets/WidgetsStatsTypeC.vue'
import WidgetsStatsD from './components/widgets/WidgetsStatsTypeD.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    MainCarousel,
    TodoList,
    // TodoMVC,
    WidgetsStatsA,
    WidgetsStatsB,
    WidgetsStatsC,
    WidgetsStatsD,
  },
})
</script>
