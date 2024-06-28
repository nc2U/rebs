<script lang="ts" setup>
import { type PropType } from 'vue'
import type { IssueProject } from '@/store/types/work'

defineProps({
  projectList: { type: Array as PropType<IssueProject[]>, default: () => [] },
})
</script>

<template>
  <CRow class="mb-3">
    <CCol>
      <v-divider class="mb-0" />
      <CTable small striped hover responsive>
        <CTableHead class="text-center">
          <CTableRow>
            <CTableHeaderCell>프로젝트</CTableHeaderCell>
            <CTableHeaderCell>역할</CTableHeaderCell>
            <CTableHeaderCell class="text-center">등록시각</CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="proj in projectList" :key="proj.pk">
            <CTableDataCell class="text-left">
              <router-link :to="{ name: '(개요)', params: { projId: proj.slug } }">
                {{ proj.name }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell></CTableDataCell>
            <CTableDataCell class="text-center">
              <!--                  {{ dateFormat(proj.members?.created, '/') }}-->
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>
</template>
