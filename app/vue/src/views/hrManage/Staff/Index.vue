<script lang="ts" setup>
import { ref, onMounted, computed, provide, readonly, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { Staff } from '@/store/types/company'
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

const fetchStaffList = (page?: number) => companyStore.fetchStaffList(page)
const fetchAllRankList = () => companyStore.fetchAllRankList()
const fetchAllDepartList = () => companyStore.fetchAllDepartList()

const createStaff = (payload: Staff, p: number) =>
  companyStore.createStaff(payload, p)
const updateStaff = (payload: Staff, p: number) =>
  companyStore.updateStaff(payload, p)
const deleteStaff = (pk: number) => companyStore.deleteStaff(pk)

const multiSubmit = (payload: Staff) => {
  if (!!payload.pk) updateStaff(payload, page.value)
  else createStaff(payload, page.value)
}
const onDelete = (pk: number) => deleteStaff(pk)

const pageSelect = (num: number) => {
  page.value = num
  fetchStaffList(num)
}

onMounted(() => {
  fetchStaffList()
  fetchAllRankList()
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
