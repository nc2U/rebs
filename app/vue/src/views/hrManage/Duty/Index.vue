<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { pageTitle, navMenu } from '@/views/hrManage/_menu/headermixin2'
import { useCompany } from '@/store/pinia/company'
import { Duty, ComFilter } from '@/store/types/company'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from './components/ListController.vue'
import AddDuty from './components/AddDuty.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import DutyList from './components/DutyList.vue'

const listControl = ref()

const dataFilter = ref<ComFilter>({
  page: 1,
  com: 1,
  q: '',
})

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const comId = computed(() => companyStore.company?.pk)
const comName = computed(() => companyStore.company?.name || undefined)

const companySelect = (target: number) => {
  if (!!target) {
    fetchDutyList({ com: target })
  } else companyStore.dutyList = []
}

const listFiltering = (payload: ComFilter) => {
  dataFilter.value = payload
  fetchDutyList({
    page: payload.page,
    com: payload.com,
    q: payload.q,
  })
}

const fetchDutyList = (payload: ComFilter) =>
  companyStore.fetchDutyList(payload)

const createDuty = (payload: Duty, p?: number, c?: number) =>
  companyStore.createDuty(payload, p, c)
const updateDuty = (payload: Duty, p?: number, c?: number) =>
  companyStore.updateDuty(payload, p, c)
const deleteDuty = (pk: number, com: number) => companyStore.deleteDuty(pk, com)

const multiSubmit = (payload: Duty) => {
  const { page } = dataFilter.value
  if (comId.value) {
    if (!!payload.pk) updateDuty(payload, page, comId.value)
    else createDuty(payload, page, comId.value)
  }
}
const onDelete = (pk: number) => {
  if (comId.value) deleteDuty(pk, comId.value)
}

const pageSelect = (num: number) => {
  dataFilter.value.page = num
  if (comId.value) {
    dataFilter.value.com = comId.value
    fetchDutyList(dataFilter.value)
  }
}

onMounted(() => {
  if (initComId.value) fetchDutyList({ com: initComId.value })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    :selector="'CompanySelect'"
    @header-select="companySelect"
  />
  <ContentBody>
    <CCardBody>
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddDuty :company="comName" @multi-submit="multiSubmit" />
      <TableTitleRow title="직책 목록" excel url="#" disabled />
      <DutyList
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @page-select="pageSelect"
      />
    </CCardBody>

    <CCardFooter class="text-right">&nbsp;</CCardFooter>
  </ContentBody>
</template>
