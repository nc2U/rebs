<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import {
  Department as Depart,
  DepFilter,
  RankFilter,
} from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddDepartment from './components/AddDepartment.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DepartmentList from './components/DepartmentList.vue'

const listControl = ref()

const dataFilter = ref<DepFilter>({
  page: 1,
  com: 1,
  upp: '',
  q: '',
})

const companyStore = useCompany()
const getPkDeparts = computed(() => companyStore.getPkDeparts)
const initComId = computed(() => companyStore.initComId)
const comId = computed(() => companyStore.company?.pk || initComId.value)
const comName = computed(() => companyStore.company?.name || undefined)

onMounted(() => {
  fetchDepartmentList({})
  fetchAllDepartList()
})

const listFiltering = (payload: DepFilter) => {
  dataFilter.value = payload
  fetchDepartmentList({
    page: payload.page,
    com: payload.com,
    upp: payload.upp,
    q: payload.q,
  })
}

const fetchDepartmentList = (payload: DepFilter) =>
  companyStore.fetchDepartmentList(payload)
const fetchAllDepartList = () => companyStore.fetchAllDepartList()

const createDepartment = (payload: Depart, p?: number, c?: number) =>
  companyStore.createDepartment(payload, p, c)
const updateDepartment = (payload: Depart, p?: number, c?: number) =>
  companyStore.updateDepartment(payload, p, c)
const deleteDepartment = (pk: number, com: number) =>
  companyStore.deleteDepartment(pk, com)

const multiSubmit = (payload: Depart) => {
  const { page } = dataFilter.value
  if (!!payload.pk) updateDepartment(payload, page)
  else {
    if (payload.upper_depart) payload.level = getLevel(payload.upper_depart)
    createDepartment(payload, page)
  }
}
const onDelete = (pk: number) => deleteDepartment(pk, comId.value)

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  dataFilter.value.com = comId.value
  fetchDepartmentList(dataFilter.value)
}

const getLevel = (up: number) =>
  getPkDeparts.value.filter(d => d.value === up)[0].level + 1
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
