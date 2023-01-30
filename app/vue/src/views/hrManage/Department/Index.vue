<script lang="ts" setup>
import { ref, onMounted, computed, provide, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddDepartment from './components/AddDepartment.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DepartmentList from './components/DepartmentList.vue'

const listControl = ref()
const departs = ref<{ value: number | undefined; label: string }[]>([])

provide('departs', departs)

const companyStore = useCompany()
const comId = computed(() => companyStore.company?.pk || null)

const getDeparts = computed(() => companyStore.getDeparts)
watch(
  () => getDeparts.value,
  nv => {
    if (!!nv) departs.value = nv
    else departs.value = []
  },
)

const fetchDepartmentList = (page?: number) =>
  companyStore.fetchDepartmentList(page)

const listFiltering = () => 1
const pageSelect = (page: number) => fetchDepartmentList(page)

onMounted(() => fetchDepartmentList())
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
      <AddDepartment />
      <TableTitleRow title="부서 목록" excel url="#" disabled />
      <DepartmentList :company="comId" @page-select="pageSelect" />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
