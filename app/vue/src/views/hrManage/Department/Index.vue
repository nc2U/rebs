<script lang="ts" setup>
import { ref, onMounted, computed, watch, provide, readonly } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Department as Depart } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddDepartment from './components/AddDepartment.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DepartmentList from './components/DepartmentList.vue'

const listControl = ref()
const departs = ref<
  {
    value: number | undefined
    label: string
    level: number
  }[]
>([])

provide('departs', readonly(departs))

const companyStore = useCompany()
const comName = computed(() => companyStore.company?.name || undefined)

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

const createDepartment = (payload: Depart) =>
  companyStore.createDepartment(payload)
const updateDepartment = (payload: Depart) =>
  companyStore.updateDepartment(payload)
const deleteDepartment = (pk: number) => companyStore.deleteDepartment(pk)

const listFiltering = () => 1

const multiSubmit = (payload: Depart) => {
  if (!!payload.pk) updateDepartment(payload)
  else {
    if (payload.upper_depart) payload.level = getLevel(payload.upper_depart)
    createDepartment(payload)
  }
}
const onDelete = (pk: number) => deleteDepartment(pk)

const pageSelect = (page: number) => fetchDepartmentList(page)

const getLevel = (up: number) =>
  departs.value.filter(d => d.value === up)[0].level + 1

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
      <AddDepartment :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="부서 목록" excel url="#" disabled />
      <DepartmentList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
