<script lang="ts" setup="">
import { computed, ref } from 'vue'
import { useCompany } from '@/store/pinia/company'
import { headerSecondary } from '@/utils/cssMixins'
import Pagination from '@/components/Pagination'
import Staff from './Staff.vue'

const emit = defineEmits(['page-select'])

const companyStore = useCompany()
const staffList = computed(() => companyStore.staffList)
const staffsCount = computed(() => companyStore.staffsCount)

const staffPages = (page: number) => companyStore.staffPages(page)
const pageSelect = (page: number) => emit('page-select', page)
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="10%" />
      <col width="10%" />
      <col width="10%" />
      <col width="11%" />
      <col width="7%" />
      <col width="10%" />
      <col width="15%" />
      <col width="15%" />
      <col width="7%" />
    </colgroup>

    <CTableHead :color="headerSecondary">
      <CTableRow class="text-center" align="middle">
        <CTableHeaderCell scope="col">No</CTableHeaderCell>
        <CTableHeaderCell scope="col">부서</CTableHeaderCell>
        <CTableHeaderCell scope="col">직책</CTableHeaderCell>
        <CTableHeaderCell scope="col">성명</CTableHeaderCell>
        <CTableHeaderCell scope="col">생년월일</CTableHeaderCell>
        <CTableHeaderCell scope="col">성별</CTableHeaderCell>
        <CTableHeaderCell scope="col">입사일</CTableHeaderCell>
        <CTableHeaderCell scope="col">휴대전화</CTableHeaderCell>
        <CTableHeaderCell scope="col">이메일</CTableHeaderCell>
        <CTableHeaderCell scope="col">상태</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <Staff v-for="staff in staffList" :key="staff.pk" :staff="staff" />
    </CTableBody>
  </CTable>

  <Pagination
    v-if="staffsCount > 10"
    :active-page="1"
    :limit="8"
    :pages="staffPages(10)"
    class="mt-3"
    @active-page-change="pageSelect"
  />
</template>
