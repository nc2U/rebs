<script lang="ts" setup>
import { computed } from 'vue'
import NoData from '@/views/_Work/components/NoData.vue'

const memberList = computed(() => [])
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <span class="mr-2">
        <v-icon icon="mdi-plus-circle" color="success" size="sm" />
        <router-link to="" class="ml-1">새 구성원</router-link>
      </span>
    </CCol>

    <CCol class="text-right">
      <span>
        <v-icon icon="mdi-cog" color="grey" size="sm" />
        <router-link :to="{ name: '사용자' }" class="ml-1">관리</router-link>
      </span>
    </CCol>
  </CRow>

  <NoData v-if="!memberList.length" />

  <CRow v-else>
    <CCol>
      <v-divider class="my-0" />
      <CTable hover small striped responsive>
        <CTableHead>
          <CTableRow class="text-center">
            <CTableHeaderCell scope="col"></CTableHeaderCell>
            <CTableHeaderCell scope="col">사용자/그룹</CTableHeaderCell>
            <CTableHeaderCell scope="col">역할</CTableHeaderCell>
            <CTableHeaderCell scope="col"></CTableHeaderCell>
          </CTableRow>
        </CTableHead>

        <CTableBody>
          <CTableRow v-for="i in 2" :key="i" class="text-center">
            <CTableHeaderCell></CTableHeaderCell>
            <CTableDataCell>
              <router-link to="">austin1 kho</router-link>
            </CTableDataCell>
            <CTableDataCell> 관리자, 개발자</CTableDataCell>
            <CTableDataCell>
              <span class="mr-2">
                <v-icon icon="mdi-pencil" color="amber" size="sm" />
                <router-link to="">편집</router-link>
              </span>
              <span>
                <v-icon icon="mdi-trash-can-outline" color="grey" size="sm" />
                <router-link to="">삭제</router-link>
              </span>
            </CTableDataCell>
          </CTableRow>
        </CTableBody>
      </CTable>
    </CCol>
  </CRow>
</template>
