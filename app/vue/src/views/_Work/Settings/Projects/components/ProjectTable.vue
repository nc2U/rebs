<script lang="ts" setup>
import type { PropType } from 'vue'
import type { IssueProject } from '@/store/types/work'

defineProps({
  issueProjectList: { type: Array as PropType<IssueProject[]>, default: () => [] },
})
</script>

<template>
  <v-divider class="mb-0" />
  <CTable hover small striped>
    <CTableHead>
      <CTableRow color="">
        <CTableHeaderCell>
          <CFormCheck />
        </CTableHeaderCell>
        <CTableHeaderCell>이름</CTableHeaderCell>
        <CTableHeaderCell>식별자</CTableHeaderCell>
        <CTableHeaderCell>설명</CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="iproj in issueProjectList" :key="iproj.pk">
        <CTableDataCell>
          <CFormCheck />
        </CTableDataCell>
        <CTableDataCell>
          <router-link :to="{ name: '(개요)', params: { projId: iproj.slug } }">
            {{ iproj.name }}
          </router-link>
        </CTableDataCell>
        <CTableDataCell>{{ iproj.slug }}</CTableDataCell>
        <CTableDataCell>{{ iproj.description }}</CTableDataCell>
        <CTableDataCell>
          <v-icon icon="mdi-dots-horizontal" />
        </CTableDataCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
