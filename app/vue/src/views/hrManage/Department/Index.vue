<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin1'
import { useCompany } from '@/store/pinia/company'
import { Department as Depart, DepFilter } from '@/store/types/company'
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

const comStore = useCompany()
const getPkDeparts = computed(() => comStore.getPkDeparts)
const comId = computed(() => comStore.company?.pk)
const comName = computed(() => comStore.company?.name || undefined)

const listFiltering = (payload: DepFilter) => {
  dataFilter.value = payload
  if (comId.value)
    fetchDepartmentList({
      page: payload.page,
      com: payload.com,
      upp: payload.upp,
      q: payload.q,
    })
}

const fetchDepartmentList = (payload: DepFilter) =>
  comStore.fetchDepartmentList(payload)
const fetchAllDepartList = (com?: number) => comStore.fetchAllDepartList(com)

const createDepartment = (payload: Depart, p?: number, c?: number) =>
  comStore.createDepartment(payload, p, c)
const updateDepartment = (payload: Depart, p?: number, c?: number) =>
  comStore.updateDepartment(payload, p, c)
const deleteDepartment = (pk: number, com: number) =>
  comStore.deleteDepartment(pk, com)

const multiSubmit = (payload: Depart) => {
  const { page } = dataFilter.value
  if (!!payload.pk) updateDepartment(payload, page)
  else {
    if (payload.upper_depart) payload.level = getLevel(payload.upper_depart)
    createDepartment(payload, page)
  }
}
const onDelete = (pk: number) => {
  if (comId.value) deleteDepartment(pk, comId.value)
}

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  if (comId.value) {
    dataFilter.value.com = comId.value
    fetchDepartmentList(dataFilter.value)
  }
}

const getLevel = (up: number) =>
  getPkDeparts.value.filter(d => d.value === up)[0].level + 1

const dataSetup = (pk: number) => {
  fetchAllDepartList(pk)
  fetchDepartmentList({ com: pk })
}

const dataReset = () => {
  comStore.departmentList = []
  comStore.allDepartList = []
}

const comSelect = (target: number | null) => {
  dataReset()
  if (!!target) dataSetup(target)
}

onMounted(() => dataSetup(comId.value || comStore.initComId))
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @com-select="comSelect"
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
