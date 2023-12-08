<script lang="ts" setup>
import { computed } from 'vue'
import { useDocument } from '@/store/pinia/document'
import MainCarousel from './components/MainCarousel.vue'
import WiseWord from '@/views/_Dashboard/components/WiseWord.vue'
import NoticeBoard from './components/NoticeBoard/ListComp.vue'
import WidgetsStatsA from './components/Widgets/WidgetsStatsTypeA.vue'
import WidgetsStatsB from './components/Widgets/WidgetsStatsTypeB.vue'
import WidgetsStatsC from './components/Widgets/WidgetsStatsTypeC.vue'

const docStore = useDocument()
const postList = computed(() => docStore.postList)
const noticeList = computed(() => docStore.noticeList)
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
        <NoticeBoard :notice-list="noticeList" :post-list="postList" />
      </CCol>
      <CCol xl="6">
        <WidgetsStatsB />
      </CCol>
    </CRow>
    <CRow>
      <CCol>
        <WidgetsStatsA />
      </CCol>
    </CRow>
    <CRow>
      <CCol>
        <WidgetsStatsC />
      </CCol>
    </CRow>
  </CContainer>
</template>
