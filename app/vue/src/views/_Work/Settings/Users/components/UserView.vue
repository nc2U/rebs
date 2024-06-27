<script lang="ts" setup>
import { useAccount } from '@/store/pinia/account'
import { computed, inject, onBeforeMount } from 'vue'
import { onBeforeRouteUpdate, useRoute } from 'vue-router'
import { dateFormat } from '@/utils/baseMixins'

const superAuth = inject('superAuth', false)

const accStore = useAccount()
const user = computed(() => accStore.user)

onBeforeRouteUpdate(async to => {
  if (to.params.userId) await accStore.fetchUser(Number(to.params.userId))
  else accStore.user = null
})
const route = useRoute()
onBeforeMount(() => {
  if (route.params.userId) accStore.fetchUser(Number(route.params.userId))
})
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="h5 mr-2" style="font-size: 1.15em">
        {{ user?.profile?.name ?? user?.username }}
      </span>
    </CCol>

    <CCol v-if="user && superAuth" class="text-right form-text">
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link :to="{ name: '사용자 - 수정', params: { userId: user.pk } }" class="ml-1">
          편집
        </router-link>
      </span>
    </CCol>
  </CRow>

  <CRow>
    <CCol>
      <CRow class="mb-3">
        <CCol class="pl-5">
          <ul>
            <li>로그인 : {{ user?.username }}</li>
            <li>등록시각 : {{ user ? dateFormat(user.date_joined, '/') : '' }}</li>
            <li>마지막 로그인 : {{ user?.last_login ? dateFormat(user.last_login, '/') : '' }}</li>
          </ul>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol>
          <h5 style="font-size: 1.15em">업무</h5>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol>
          <v-divider class="mb-0" />
          <CTable small striped hover responsive class="text-center">
            <CTableHead>
              <CTableRow>
                <CTableHeaderCell></CTableHeaderCell>
                <CTableHeaderCell>진행중</CTableHeaderCell>
                <CTableHeaderCell>완료됨</CTableHeaderCell>
                <CTableHeaderCell>합계</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow>
                <CTableDataCell class="text-left">할당된 업무</CTableDataCell>
                <CTableDataCell>a</CTableDataCell>
                <CTableDataCell></CTableDataCell>
                <CTableDataCell></CTableDataCell>
              </CTableRow>
              <CTableRow>
                <CTableDataCell class="text-left">보고한 업무</CTableDataCell>
                <CTableDataCell>a</CTableDataCell>
                <CTableDataCell></CTableDataCell>
                <CTableDataCell></CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>
        </CCol>
      </CRow>

      <CRow>
        <CCol>
          <h5 style="font-size: 1.15em">프로젝트</h5>
        </CCol>
      </CRow>
      <CRow>
        <CCol>
          <v-divider class="mb-0" />
          <CTable small striped hover responsive>
            <CTableHead class="text-center">
              <CTableRow>
                <CTableHeaderCell>프로젝트</CTableHeaderCell>
                <CTableHeaderCell>역할</CTableHeaderCell>
                <CTableHeaderCell>등록시각</CTableHeaderCell>
              </CTableRow>
            </CTableHead>
            <CTableBody>
              <CTableRow>
                <CTableDataCell class="text-left">a</CTableDataCell>
                <CTableDataCell></CTableDataCell>
                <CTableDataCell></CTableDataCell>
              </CTableRow>
              <CTableRow>
                <CTableDataCell class="text-left">a</CTableDataCell>
                <CTableDataCell></CTableDataCell>
                <CTableDataCell></CTableDataCell>
              </CTableRow>
            </CTableBody>
          </CTable>
        </CCol>
      </CRow>
    </CCol>
    <CCol class="pl-2">
      <CRow>
        <CCol>
          <h5 style="font-size: 1.15em">
            <router-link :to="{ name: '작업내역' }">작업내역</router-link>
          </h5>
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>
