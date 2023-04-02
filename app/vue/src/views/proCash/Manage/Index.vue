<script lang="ts" setup>
import { ref, computed, onBeforeMount } from 'vue'
import { pageTitle, navMenu } from '@/views/proCash/_menu/headermixin'
import { useComCash } from '@/store/pinia/comCash'
import { useProCash } from '@/store/pinia/proCash'
import { useProject } from '@/store/pinia/project'
import {
  CashBookFilter,
  ProBankAcc,
  ProjectCashBook as PrCashBook,
} from '@/store/types/proCash'
import { cutString } from '@/utils/baseMixins'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import ListController from '@/views/proCash/Manage/components/ListController.vue'
import AddProCash from '@/views/proCash/Manage/components/AddProCash.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import ProCashList from '@/views/proCash/Manage/components/ProCashList.vue'

const listControl = ref()

const dataFilter = ref<CashBookFilter>({
  page: 1,
  from_date: '',
  to_date: '',
  sort: null,
  pro_acc_d2: null,
  pro_acc_d3: null,
  bank_account: null,
  search: '',
})

const pageSelect = (page: number) => {
  dataFilter.value.page = page
  listControl.value.listFiltering(page)
}

const listFiltering = (payload: CashBookFilter) => {
  dataFilter.value = payload
  const sort = payload.sort ? payload.sort : null
  const d1 = payload.pro_acc_d2 ? payload.pro_acc_d2 : null
  fetchProFormAccD1List(sort)
  fetchProFormAccD3List(d1, sort)
  fetchProjectCashList({ ...{ project: project.value }, ...payload })
}

const excelSelect = '1'

const excelUrl = computed(() => {
  const pj = project.value
  const sd = dataFilter.value.from_date
  const ed = dataFilter.value.to_date
  const st = dataFilter.value.sort || ''
  const d1 = dataFilter.value.pro_acc_d2 || ''
  const d2 = dataFilter.value.pro_acc_d3 || ''
  const ba = dataFilter.value.bank_account || ''
  const q = dataFilter.value.search
  return `/excel/p-cashbook/?project=${pj}&sdate=${sd}&edate=${ed}&sort=${st}&d1=${d1}&d2=${d2}&bank_acc=${ba}&q=${q}`
})

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const comCashStore = useComCash()
const fetchBankCodeList = () => comCashStore.fetchBankCodeList()

const proCashStore = useProCash()
const fetchProAccSortList = () => proCashStore.fetchProAccSortList()
const fetchProAllAccD1List = () => proCashStore.fetchProAllAccD1List()
const fetchProAllAccD3List = () => proCashStore.fetchProAllAccD3List()

const fetchProFormAccD1List = (sort?: number | null) =>
  proCashStore.fetchProFormAccD1List(sort)
const fetchProFormAccD3List = (d1?: number | null, sort?: number | null) =>
  proCashStore.fetchProFormAccD3List(d1, sort)

const fetchProBankAccList = (projId: number) =>
  proCashStore.fetchProBankAccList(projId)
const fetchAllProBankAccList = (projId: number) =>
  proCashStore.fetchAllProBankAccList(projId)
const fetchProjectCashList = (payload: { project: number }) =>
  proCashStore.fetchProjectCashList(payload)

const patchProBankAcc = (payload: ProBankAcc) =>
  proCashStore.patchProBankAcc(payload)

const createPrCashBook = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.createPrCashBook(payload)

const updatePrCashBook = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => proCashStore.updatePrCashBook(payload)

const deletePrCashBook = (
  payload: { pk: number; project: number } & {
    filters?: CashBookFilter
  },
) => proCashStore.deletePrCashBook(payload)

const onSelectAdd = (target: number) => {
  if (!!target) {
    fetchProBankAccList(target)
    fetchAllProBankAccList(target)
    fetchProjectCashList({ project: target })
  } else {
    proCashStore.proBankAccountList = []
    proCashStore.allProBankAccountList = []
    proCashStore.proCashBookList = []
    proCashStore.proCashesCount = 0
  }
}

const chargeCreate = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
  charge: number,
) => {
  payload.sort = 2
  payload.project_account_d2 = 9
  payload.project_account_d3 = 43
  payload.content = cutString(payload.content, 8) + ' - 이체수수료'
  payload.trader = '지급수수료'
  payload.outlay = charge
  payload.income = null
  payload.evidence = '0'
  payload.note = ''

  createPrCashBook(payload)
}

const onCreate = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  } & { bank_account_to: null | number; charge: null | number },
) => {
  payload.project = project.value
  if (payload.sort === 3 && payload.bank_account_to) {
    // 대체 거래일 때
    const { bank_account, bank_account_to, charge, ...inputData } = payload

    inputData.sort = 2
    inputData.trader = '내부대체'
    inputData.project_account_d3 = 67
    createPrCashBook({ bank_account, ...inputData })

    inputData.sort = 1
    inputData.project_account_d3 += 1
    inputData.income = inputData.outlay
    inputData.outlay = null

    setTimeout(
      () => createPrCashBook({ bank_account: bank_account_to, ...inputData }),
      300,
    )
    if (!!charge) {
      setTimeout(
        () => chargeCreate({ bank_account, ...inputData }, charge),
        600,
      )
    }
  } else if (payload.sort === 4) {
    // 취소 거래일 때
    payload.sort = 2
    payload.project_account_d3 = 69
    payload.evidence = '0'
    createPrCashBook(payload)
    payload.sort = 1
    payload.project_account_d3 += 1
    payload.income = payload.outlay
    delete payload.outlay
    payload.evidence = ''
    setTimeout(() => createPrCashBook(payload), 300)
  } else {
    const { charge, ...inputData } = payload
    createPrCashBook(inputData)
    if (!!charge) chargeCreate(inputData, charge)
  }
}

const onUpdate = (
  payload: PrCashBook & { sepData: PrCashBook | null } & {
    filters: CashBookFilter
  },
) => updatePrCashBook(payload)

const multiSubmit = (payload: {
  formData: PrCashBook
  sepData: PrCashBook | null
  bank_account_to: null | number
  charge: null | number
}) => {
  const { formData, ...sepData } = payload
  const submitData = {
    ...formData,
    ...sepData,
    ...{ filters: dataFilter.value },
  }

  if (formData.pk) onUpdate(submitData)
  else onCreate(submitData)
}

const onDelete = (payload: { pk: number; project: number }) =>
  deletePrCashBook({ ...{ filters: dataFilter.value }, ...payload })

const onBankUpdate = (payload: ProBankAcc) => patchProBankAcc(payload)

onBeforeMount(() => {
  fetchBankCodeList()
  fetchProAccSortList()
  fetchProAllAccD1List()
  fetchProAllAccD3List()
  fetchProFormAccD1List()
  fetchProFormAccD3List()
  fetchProBankAccList(project.value)
  fetchAllProBankAccList(project.value)
  fetchProjectCashList({ project: project.value })
})
</script>

<template>
  <ContentHeader
    :page-title="pageTitle"
    :nav-menu="navMenu"
    @header-select="onSelectAdd"
  />

  <ContentBody>
    <CCardBody class="pb-5">
      <ListController ref="listControl" @list-filtering="listFiltering" />
      <AddProCash @multi-submit="multiSubmit" @onBankUpdate="onBankUpdate" />
      <TableTitleRow
        title="프로젝트 입출금 내역"
        color="indigo"
        excel
        :url="excelUrl"
      >
        <v-radio-group
          v-model="excelSelect"
          inline
          size="sm"
          density="compact"
          class="d-flex flex-row-reverse"
          style="font-size: 0.8em"
        >
          <v-radio label="전체(운영비용 포함)" value="1" />
        </v-radio-group>
      </TableTitleRow>
      <ProCashList
        @page-select="pageSelect"
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @onBankUpdate="onBankUpdate"
      />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
