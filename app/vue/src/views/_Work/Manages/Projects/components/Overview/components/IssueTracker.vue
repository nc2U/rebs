<script lang="ts" setup>
import { inject } from 'vue'

const isDark = inject('isDark')
</script>

<template>
  <CCard :color="isDark ? '' : 'light'">
    <CCardBody>
      <CCardSubtitle>업무 추적</CCardSubtitle>
      <CTable bordered hover small striped class="mt-2 mb-0">
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col"></CTableHeaderCell>
            <CTableHeaderCell scope="col">진행중</CTableHeaderCell>
            <CTableHeaderCell scope="col">완료됨</CTableHeaderCell>
            <CTableHeaderCell scope="col">합계</CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="i in 3" :key="i" class="text-center">
            <CTableHeaderCell>결함</CTableHeaderCell>
            <CTableDataCell>0</CTableDataCell>
            <CTableDataCell>0</CTableDataCell>
            <CTableDataCell>0</CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCardBody>

    <CCardText class="mx-3 mb-2"> 모든 업무 보기 | 요약 | 달력 | Gantt 차트</CCardText>
  </CCard>
</template>
