<script lang="ts" setup>
import type { PropType } from 'vue'
import type { Issue } from '@/store/types/work'
import { timeFormat } from '@/utils/baseMixins'
import NoData from '@/views/_Work/components/NoData.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'

defineProps({
  issueList: { type: Array as PropType<Issue[]>, default: () => [] },
})
</script>

<template>
  <CRow>
    <CRow class="py-2">
      <CCol>
        <h5>{{ $route.name }}</h5>
      </CCol>

      <CCol class="text-right">
        <span class="mr-2">
          <v-icon icon="mdi-plus-circle" color="success" size="sm" />
          <router-link :to="{ name: '업무 - 추가' }" class="ml-1">새 업무만들기</router-link>
        </span>
      </CCol>
    </CRow>

    <SearchList />

    <NoData v-if="!issueList.length" />

    <CCol v-else col="12">
      <v-divider class="mb-0" />
      <CTable striped hover small>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col">#</CTableHeaderCell>
            <CTableHeaderCell scope="col">프로젝트</CTableHeaderCell>
            <CTableHeaderCell scope="col">유형</CTableHeaderCell>
            <CTableHeaderCell scope="col">상태</CTableHeaderCell>
            <CTableHeaderCell scope="col">우선순위</CTableHeaderCell>
            <CTableHeaderCell scope="col">제목</CTableHeaderCell>
            <CTableHeaderCell scope="col">담당자</CTableHeaderCell>
            <CTableHeaderCell scope="col">변경</CTableHeaderCell>
            <CTableHeaderCell scope="col"></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="issue in issueList" :key="issue.pk">
            <CTableDataCell>
              <router-link
                :to="{
                  name: '(업무) - 보기',
                  params: { projId: issue.project.slug, issueId: issue.pk },
                }"
              >
                {{ issue.pk }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell>
              <router-link :to="{ name: '(개요)', params: { projId: issue.project.slug } }">
                {{ issue.project.name }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell>{{ issue.tracker.name }}</CTableDataCell>
            <CTableDataCell>{{ issue.status.name }}</CTableDataCell>
            <CTableDataCell>{{ issue.priority.name }}</CTableDataCell>
            <CTableDataCell>
              <router-link
                :to="{
                  name: '(업무) - 보기',
                  params: { projId: issue.project.slug, issueId: issue.pk },
                }"
              >
                {{ issue.subject }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell class="text-center">
              <router-link
                :to="{ name: '사용자 - 보기', params: { userId: issue.assigned_to?.pk } }"
              >
                {{ issue.assigned_to?.username }}
              </router-link>
            </CTableDataCell>
            <CTableDataCell class="text-center">{{ timeFormat(issue.updated) }}</CTableDataCell>
            <CTableDataCell></CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>
</template>
