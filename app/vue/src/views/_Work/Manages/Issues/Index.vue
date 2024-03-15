<script setup lang="ts">
import { computed, type ComputedRef, inject, onBeforeMount, ref } from 'vue'
import { navMenu2 as navMenu } from '@/views/_Work/_menu/headermixin1'
import { timeFormat } from '@/utils/baseMixins'
import type { Company } from '@/store/types/settings'
import { useWork } from '@/store/pinia/work'
import Header from '@/views/_Work/components/Header/Index.vue'
import ContentBody from '@/views/_Work/components/ContentBody/Index.vue'
import SearchList from '@/views/_Work/components/SearchList.vue'
import NoData from '@/views/_Work/components/NoData.vue'

const cBody = ref()
const company = inject<ComputedRef<Company>>('company')
const comName = computed(() => company?.value?.name)

const sideNavCAll = () => cBody.value.toggle()

const workStore = useWork()
const issueList = computed(() => workStore.issueList)

onBeforeMount(() => {
  workStore.fetchIssueList()
})
</script>

<template>
  <Header :page-title="comName" :nav-menu="navMenu" @side-nav-call="sideNavCAll" />

  <ContentBody ref="cBody" :nav-menu="navMenu" :query="$route?.query">
    <template v-slot:default>
      <CRow class="py-2">
        <CCol>
          <h5>{{ $route.name }}</h5>
        </CCol>

        <CCol class="text-right">
          <span v-show="$route.name !== '프로젝트 - 추가'" class="mr-2">
            <v-icon icon="mdi-plus-circle" color="success" size="sm" />
            <router-link to="" class="ml-1">새 업무만들기</router-link>
          </span>
        </CCol>
      </CRow>

      <SearchList />

      <NoData v-if="!issueList.length" />

      <CRow v-else>
        <CCol col="12">
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
                <CTableDataCell>{{ issue.tracker }}</CTableDataCell>
                <CTableDataCell>{{ issue.status }}</CTableDataCell>
                <CTableDataCell>{{ issue.priority }}</CTableDataCell>
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
                    :to="{ name: '사용자 - 보기', params: { userId: issue.assigned_to.pk } }"
                  >
                    {{ issue.assigned_to.username }}
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

    <template v-slot:aside></template>
  </ContentBody>
</template>
