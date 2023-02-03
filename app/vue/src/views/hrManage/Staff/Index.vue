<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin1'
import { useCompany } from '@/store/pinia/company'
import { Staff, StaffFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddStaff from './components/AddStaff.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StaffList from './components/StaffList.vue'
import { useAccount } from '@/store/pinia/account'

const listControl = ref()

const dataFilter = ref<StaffFilter>({
  page: 1,
  com: 1,
  sort: '2',
  dep: '',
  gra: '',
  pos: '',
  dut: '',
  sts: '',
  q: '',
})

const comStore = useCompany()
const initComId = computed(() => comStore.initComId)
const comId = computed(() => comStore.company?.pk || initComId.value)
const comName = computed(() => comStore.company?.name || undefined)

const accStore = useAccount()
const fetchUsersList = () => accStore.fetchUsersList()

onMounted(() => {
  fetchStaffList({ com: comId.value })
  fetchAllGradeList(comId.value)
  fetchAllDepartList(comId.value)
  fetchAllPositionList(comId.value)
  fetchAllDutyList(comId.value)
  fetchUsersList()
})

const listFiltering = (payload: StaffFilter) => {
  dataFilter.value = payload
  fetchStaffList({
    page: payload.page,
    com: payload.com,
    sort: payload.sort,
    dep: payload.dep,
    gra: payload.gra,
    pos: payload.pos,
    dut: payload.dut,
    sts: payload.sts,
    q: payload.q,
  })
}

const fetchStaffList = (payload: StaffFilter) =>
  comStore.fetchStaffList(payload)
const fetchAllGradeList = (com?: number) => comStore.fetchAllGradeList(com)
const fetchAllDepartList = (com?: number) => comStore.fetchAllDepartList(com)
const fetchAllPositionList = (com?: number) =>
  comStore.fetchAllPositionList(com)
const fetchAllDutyList = (com?: number) => comStore.fetchAllDutyList(com)

const createStaff = (payload: Staff, p?: number, c?: number) =>
  comStore.createStaff(payload, p, c)
const updateStaff = (payload: Staff, p?: number, c?: number) =>
  comStore.updateStaff(payload, p, c)
const deleteStaff = (pk: number, com: number) => comStore.deleteStaff(pk, com)

const multiSubmit = (payload: Staff) => {
  const { page } = dataFilter.value
  if (!!payload.pk) updateStaff(payload, page, comId.value)
  else createStaff(payload, page, comId.value)
}
const onDelete = (pk: number) => deleteStaff(pk, comId.value)

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  dataFilter.value.com = comId.value
  fetchStaffList(dataFilter.value)
}
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
