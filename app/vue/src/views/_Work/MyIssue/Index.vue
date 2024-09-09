<script setup lang="ts">
import { reactive } from 'vue'
import { GridLayout } from 'grid-layout-plus'

const layout = reactive([
  { x: 0, y: 0, w: 6, h: 3, i: '0' },
  { x: 6, y: 0, w: 6, h: 3, i: '1' },
])
</script>

<template>
  <CCard>
    <CCardBody>
      <CRow>
        <CCol>
          <CFormSelect style="width: 200px" class="align-self-end">
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
      <!-- Item slot usage -->
      <GridLayout
        v-model:layout="layout"
        :col-num="12"
        :row-height="30"
        is-draggable
        is-resizable
        vertical-compact
        use-css-transforms
      >
        <template #item="{ item }">
          <div class="w-100 h-100 border p-3">
            <CRow class="text-right px-2 mb-1">
              <CCol>{{ item.i }}</CCol>
            </CRow>
            <CAlert color="warning">표시할 데이터가 없습니다.</CAlert>
          </div>
        </template>
      </GridLayout>
    </CCardBody>
  </CCard>
</template>
