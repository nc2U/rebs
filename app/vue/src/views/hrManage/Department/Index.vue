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

const page = ref(1)
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
const DDeparts = computed(() => companyStore.DDeparts)
watch(
  () => DDeparts.value,
  nv => {
    if (!!nv) departs.value = nv
    else departs.value = []
  },
)

const listFiltering = () => 1

const fetchDepartmentList = (page?: number) =>
  companyStore.fetchDepartmentList(page)
const fetchAllDepartList = () => companyStore.fetchAllDepartList()

const createDepartment = (payload: Depart, p: number) =>
  companyStore.createDepartment(payload, p)
const updateDepartment = (payload: Depart, p: number) =>
  companyStore.updateDepartment(payload, p)
const deleteDepartment = (pk: number) => companyStore.deleteDepartment(pk)

const multiSubmit = (payload: Depart) => {
  if (!!payload.pk) updateDepartment(payload, page.value)
  else {
    if (payload.upper_depart) payload.level = getLevel(payload.upper_depart)
    createDepartment(payload, page.value)
  }
}
const onDelete = (pk: number) => deleteDepartment(pk)

const pageSelect = (num: number) => {
  page.value = num
  fetchDepartmentList(num)
}

const getLevel = (up: number) =>
  departs.value.filter(d => d.value === up)[0].level + 1

onMounted(() => {
  fetchDepartmentList()
  fetchAllDepartList()
})
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
