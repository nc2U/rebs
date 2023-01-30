<script lang="ts" setup="">
import { computed } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { headerSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Department from './Department.vue'

const emit = defineEmits(['page-select'])

const companyStore = useCompany()
const departmentList = computed(() => companyStore.departmentList)
const departs = computed(() =>
  departmentList.value.map(d => ({ pk: d.pk, name: d.name })),
)
const departmentsCount = computed(() => companyStore.departmentsCount)

const departmentPages = (page: number) => companyStore.departmentPages(page)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="10%" />
      <col width="20%" />
      <col width="20%" />
      <col width="50%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">상위부서</CTableHeaderCell>
        <CTableHeaderCell scope="col">부서명</CTableHeaderCell>
        <CTableHeaderCell scope="col">주요업무</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Department
        v-for="depart in departmentList"
        :key="depart.pk"
        :department="depart"
        :departs="departs"
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
