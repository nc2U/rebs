<script setup lang="ts">
import { reactive } from 'vue'
import { GridItem, GridLayout } from 'grid-layout-plus'

const layout = reactive([
  { x: 0, y: 0, w: 6, h: 4, i: '0' },
  { x: 6, y: 0, w: 6, h: 4, i: '1' },
])
</script>

<template>
  <CCard>
    <CCardBody>
      <CRow class="text-right">
        <CCol class="text-right">
          <CFormSelect style="width: 200px">
            <option>추가하기</option>
            <option>내가 맡은 업무</option>
            <option>보고한 업무</option>
            <option>수정한 업무</option>
            <option>지켜보고 있는 업무</option>
            <option>업무</option>
            <option>최근 뉴스</option>
            <option>달력</option>
            <option>문서</option>
            <option>소요시간</option>
            <option>작업내역</option>
          </CFormSelect>
        </CCol>
      </CRow>
      <!-- Default slot usage -->
      <GridLayout
        v-model:layout="layout"
        :col-num="12"
        :row-height="30"
        is-draggable
        :is-resizable="false"
        vertical-compact
        use-css-transforms
      >
        <GridItem
          v-for="item in layout"
          :key="item.i"
          :x="item.x"
          :y="item.y"
          :w="item.w"
          :h="item.h"
          :i="item.i"
          class="bg-light"
        >
          {{ item.i }}
        </GridItem>
      </GridLayout>
    </CCardBody>
  </CCard>
</template>
