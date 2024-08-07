<script lang="ts" setup>
import { computed } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { TableSecondary } from '@/utils/cssMixins'
import { write_human_resource } from '@/utils/pageAuth'
import { type Department as Depart } from '@/store/types/company'
import Pagination from '@/components/Pagination'
import Department from './Department.vue'

const emit = defineEmits(['page-select', 'multi-submit', 'on-delete'])

const companyStore = useCompany()
const getPkDeparts = computed(() => companyStore.getPkDeparts)
const departmentList = computed(() => companyStore.departmentList)
const departmentsCount = computed(() => companyStore.departmentsCount)

const departmentPages = (page: number) => companyStore.departmentPages(page)
const pageSelect = (page: number) => emit('page-select', page)
const multiSubmit = (payload: Depart) => emit('multi-submit', payload)
const onDelete = (pk: number) => emit('on-delete', pk)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col style="width: 7%" />
      <col style="width: 15%" />
      <col style="width: 15%" />
      <col style="width: 56%" />
      <col v-if="write_human_resource" style="width: 7%" />
    </colgroup>

    <CTableHead :color="TableSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">상위부서</CTableHeaderCell>
        <CTableHeaderCell scope="col">부서명</CTableHeaderCell>
        <CTableHeaderCell scope="col">주요업무</CTableHeaderCell>
        <CTableHeaderCell v-if="write_human_resource" scope="col">비고</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Department
        v-for="depart in departmentList"
        :key="depart.pk"
        :department="depart"
        :get-departs="getPkDeparts"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
      />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="departmentsCount > 10"
    :active-page="1"
    :limit="8"
    :pages="departmentPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
