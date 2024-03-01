<script lang="ts" setup>
import { computed, onBeforeMount } from 'vue'
import { useWork } from '@/store/pinia/work'

const emit = defineEmits(['aside-visible'])

const workStore = useWork()
const iProject = computed(() => workStore.issueProject)

onBeforeMount(() => emit('aside-visible', false))
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
      </CRow>
    </CCol>

    <CCol>
      <CCard v-if="iProject?.sub_projects?.length">
        <CCardBody>
          <CCardSubtitle>하위 프로젝트</CCardSubtitle>
          <CCardText>
            <router-link
              v-for="(sub, i) in iProject.sub_projects"
              :to="{ name: '(개요)', params: { projId: sub.slug } }"
              :key="sub.pk"
            >
              {{ sub.name }}<span v-if="i + 1 < iProject?.sub_projects?.length">, </span>
            </router-link>
          </CCardText>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>

  <CRow>
    <CCol>{{ iProject }}</CCol>
  </CRow>
</template>
