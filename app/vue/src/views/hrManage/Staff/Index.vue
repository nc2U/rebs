<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddStaff from './components/AddStaff.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StaffList from './components/StaffList.vue'

const listControl = ref()

const companyStore = useCompany()
const fetchStaffList = (page?: number) => companyStore.fetchStaffList(page)

const listFiltering = () => 1
const pageSelect = (page: number) => fetchStaffList(page)

onMounted(() => fetchStaffList())
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
  />
  <ContentBody>
    <CCardBody>
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddStaff />
      <TableTitleRow title="직원 목록" excel url="#" disabled />
      <StaffList @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
