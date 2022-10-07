<script lang="ts" setup>
import { computed, onBeforeMount, ref } from 'vue'
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

const companyStore = useCompany()
const initComId = computed(() => companyStore.initComId)
const company = computed(() => companyStore.company?.pk || initComId.value)

const comCashStore = useComCash()
const fetchAccSortList = () => comCashStore.fetchAccSortList()
const fetchAllAccD1List = () => comCashStore.fetchAllAccD1List()
const fetchAllAccD2List = () => comCashStore.fetchAllAccD2List()
const fetchAllAccD3List = () => comCashStore.fetchAllAccD3List()

onBeforeMount(() => {
  fetchAccSortList()
  fetchAllAccD1List()
  fetchAllAccD2List()
  fetchAllAccD3List()
  fetchComBankAccList(initComId.value)
  fetchComBalanceByAccList({ company: initComId.value })
  fetchDateCashBookList({
    company: initComId.value,
    date: dateFormat(date.value),
  })
})

const fetchComBankAccList = (com: number) =>
  comCashStore.fetchComBankAccList(com)
const fetchComBalanceByAccList = (com: { company: number; date?: string }) =>
  comCashStore.fetchComBalanceByAccList(com)
const fetchDateCashBookList = (payload: { company: number; date: string }) =>
  comCashStore.fetchDateCashBookList(payload)

const excelUrl = computed(() => {
  const comp = compName.value
  let url = ''
  if (comp === 'StatusByAccount') url = `/excel/balance/`
  else if (comp === 'CashListByDate') url = `/excel/daily-cash/`
  return `${url}?&date=${dateFormat(date.value)}`
})

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchComBankAccList(target)
    fetchComBalanceByAccList({
      company: target,
      date: dateFormat(date.value),
    })
    fetchDateCashBookList({
      company: target,
      date: dateFormat(date.value),
    })
  } else {
    comCashStore.comBankList = []
    comCashStore.comBalanceByAccList = []
    comCashStore.dateCashBook = []
  }
}

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
  fetchComBalanceByAccList({
    company: company.value,
    date: dateFormat(dt),
  })
  fetchDateCashBookList({
    company: company.value,
    date: dateFormat(dt),
  })
}
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    selector="CompanySelect"
    @header-select="onSelectAdd"
  />
  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TabSelect @tab-select="showTab" />

      <TableTitleRow excel :url="excelUrl" />

      <StatusByAccount v-if="compName === 'StatusByAccount'" :date="date" />
      <CashListByDate v-if="compName === 'CashListByDate'" :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
