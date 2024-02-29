<script lang="ts" setup>
import { computed } from 'vue'
import { useWork } from '@/store/pinia/work'

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>개요</h5>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CRow class="mb-2">
        <CCol>{{ iProject?.description }}</CCol>
      </CRow>

      <CRow>
        <CCard>
          <CCardBody>
            <!--        <CCardTitle>업무 추적</CCardTitle>-->
            <CCardTitle>업무 추적</CCardTitle>
            <CTable>
              <CTableHead>
                <CTableRow class="text-center">
                  <CTableHeaderCell scope="col"></CTableHeaderCell>
                  <CTableHeaderCell scope="col">진행중</CTableHeaderCell>
                  <CTableHeaderCell scope="col">완료됨</CTableHeaderCell>
                  <CTableHeaderCell scope="col">합계</CTableHeaderCell>
                </CTableRow>
              </CTableHead>

              <CTableBody>
                <CTableRow class="text-center">
                  <CTableHeaderCell>결함</CTableHeaderCell>
                  <CTableDataCell>0</CTableDataCell>
                  <CTableDataCell>0</CTableDataCell>
                  <CTableDataCell>0</CTableDataCell>
                </CTableRow>
              </CTableBody>
            </CTable>
          </CCardBody>

          <CCardText> 모든 업무 보기 | 요약</CCardText>
        </CCard>
      </CRow>
    </CCol>

    <CCol></CCol>
  </CRow>

  <!--  <CRow>-->
  <!--    <CCol>{{ iProject }}</CCol>-->
  <!--  </CRow>-->
</template>
