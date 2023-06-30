<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { pageTitle, navMenu } from '@/views/comCash/_menu/headermixin'
import { useCompany } from '@/store/pinia/company'
import { useComCash } from '@/store/pinia/comCash'
import { dateFormat } from '@/utils/baseMixins'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/comCash/Status/components/DateChoicer.vue'
import TabSelect from '@/views/comCash/Status/components/TabSelect.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import StatusByAccount from '@/views/comCash/Status/components/StatusByAccount.vue'
import CashListByDate from '@/views/comCash/Status/components/CashListByDate.vue'

const date = ref(new Date())
const compName = ref('StatusByAccount')

const comStore = useCompany()
const company = computed(() => comStore.company?.pk)
watch(company, val => (!!val ? dataSet(val) : dataReset()))

const cashStore = useComCash()
const fetchAccSortList = () => cashStore.fetchAccSortList()
const fetchAllAccD1List = () => cashStore.fetchAllAccD1List()
const fetchAllAccD2List = () => cashStore.fetchAllAccD2List()
const fetchAllAccD3List = () => cashStore.fetchAllAccD3List()

const fetchComBankAccList = (com: number) => cashStore.fetchComBankAccList(com)
const fetchComBalanceByAccList = (com: { company: number; date: string }) =>
  cashStore.fetchComBalanceByAccList(com)
const fetchDateCashBookList = (payload: { company: number; date: string }) =>
  cashStore.fetchDateCashBookList(payload)

const excelUrl = computed(() => {
  const comp = compName.value
  let url = ''
  if (comp === 'StatusByAccount') url = `/excel/balance/`
  else if (comp === 'CashListByDate') url = `/excel/daily-cash/`
  return `${url}?&date=${dateFormat(date.value)}`
})

const showTab = (num: number) => {
  const comp: { [key: number]: string } = {
    1: 'StatusByAccount',
    2: 'CashListByDate',
  }
  compName.value = comp[num]
}

const setDate = (d: string) => {
  const dt = new Date(d)
  date.value = new Date(dt)
  if (company.value) {
    fetchComBalanceByAccList({
      company: company.value,
      date: dateFormat(dt),
    })
    fetchDateCashBookList({
      company: company.value,
      date: dateFormat(dt),
    })
  }
}

const dataSet = (pk: number) => {
  fetchComBankAccList(pk)
  fetchComBalanceByAccList({
    company: pk,
    date: dateFormat(date.value),
  })
  fetchDateCashBookList({
    company: pk,
    date: dateFormat(date.value),
  })
}

const dataReset = () => {
  cashStore.comBankList = []
  cashStore.comBalanceByAccList = []
  cashStore.dateCashBook = []
}

onBeforeMount(() => {
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  dataSet(company.value || comStore.initComId)
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TabSelect @tab-select="showTab" />

      <TableTitleRow excel :url="excelUrl" :disabled="!company" />

      <StatusByAccount v-if="compName === 'StatusByAccount'" :date="date" />
      <CashListByDate v-if="compName === 'CashListByDate'" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
