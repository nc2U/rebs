<script lang="ts" setup>
import { ref, onMounted, computed, provide, readonly, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Staff, StaffFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddStaff from './components/AddStaff.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StaffList from './components/StaffList.vue'

const page = ref<number>(1)
const listControl = ref()

const staffDeparts = ref<
  {
    value: string
    label: string
  }[]
>([])
const ranks = ref<
  {
    value: string
    label: string
  }[]
>([])
provide('staffDeparts', readonly(staffDeparts))
provide('ranks', readonly(ranks))

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const comId = computed(() => companyStore.company?.pk || initComId.value)
const comName = computed(() => companyStore.company?.name || undefined)
const SDeparts = computed(() => companyStore.SDeparts)
const getRanks = computed(() => companyStore.getRanks)
watch(
  () => SDeparts.value,
  nv => {
    if (!!nv) staffDeparts.value = nv
    else staffDeparts.value = []
  },
)
watch(
  () => getRanks.value,
  nv => {
    if (!!nv) ranks.value = nv
    else ranks.value = []
  },
)

const listFiltering = () => 1

const fetchStaffList = (payload: StaffFilter) =>
  companyStore.fetchStaffList(payload)
const fetchAllRankList = (com?: number) => companyStore.fetchAllRankList(com)
const fetchAllDepartList = (com?: number) =>
  companyStore.fetchAllDepartList(com)

const createStaff = (payload: Staff, p?: number, c?: number) =>
  companyStore.createStaff(payload, p, c)
const updateStaff = (payload: Staff, p?: number, c?: number) =>
  companyStore.updateStaff(payload, p, c)
const deleteStaff = (pk: number, com?: number) =>
  companyStore.deleteStaff(pk, com)

const multiSubmit = (payload: Staff) => {
  if (!!payload.pk) updateStaff(payload, page.value, comId.value)
  else createStaff(payload, page.value, comId.value)
}
const onDelete = (pk: number) => deleteStaff(pk, comId.value)

const pageSelect = (num: number) => {
  page.value = num
  fetchStaffList({ page: num, com: comId.value })
}

onMounted(() => {
  fetchStaffList({ com: comId.value })
  fetchAllRankList(comId.value)
  fetchAllDepartList(comId.value)
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
      <AddStaff :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직원 목록" excel url="#" disabled />
      <StaffList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
