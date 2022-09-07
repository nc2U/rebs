import api from '@/api'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { message, errorHandle } from '@/utils/helper'
import { AccountSort } from '@/store/types/comCash'
import {
  ProjectAccountD1,
  ProjectAccountD2,
  ProjectBankAccount,
  BalanceByAccount,
  ProjectCashBook,
  ProjectBudget,
  ExecAmountToBudget,
} from '@/store/types/proCash'

export const useProCash = defineStore('proCash', () => {
  // state & getters
  const sortList = ref<AccountSort[]>([])

  const fetchProAccSortList = () =>
    api
      .get(`/project-acc-sort/`)
      .then(res => (sortList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD1List = ref<ProjectAccountD1[]>([])

  const fetchProAllAccD1List = () =>
    api
      .get(`/project-account-depth1/`)
      .then(res => (allAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const allAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProAllAccD2List = () =>
    api
      .get(`/project-account-depth2/`)
      .then(res => (allAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const formAccD1List = ref<ProjectAccountD1[]>([])

  const fetchProFormAccD1List = (sort = '') =>
    api
      .get(`/project-account-depth1/?projectaccountsort=${sort}`)
      .then(res => (formAccD1List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const formAccD2List = ref<ProjectAccountD2[]>([])

  const fetchProFormAccD2List = (d1 = '', sort = '') => {
    const sortUri = sort
      ? `&d1__projectaccountsort=${sort}`
      : '&d1__projectaccountsort=1&d1__projectaccountsort=2&d1__projectaccountsort=3'
    return api
      .get(`/project-account-depth2/?d1=${d1}${sortUri}`)
      .then(res => (formAccD2List.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proBankAccountList = ref<ProjectBankAccount[]>([])

  const fetchProBankAccList = (project: number) =>
    api
      .get(`/project-bank-account/?project=${project}`)
      .then(res => (proBankAccountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const createProBankAcc = (payload: ProjectBankAccount) =>
    api
      .post(`/project-bank-account/`, payload)
      .then(res => fetchProBankAccList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const updateProBankAcc = (payload: ProjectBankAccount) =>
    api
      .put(`/project-bank-account/${payload.pk}/`, payload)
      .then(res => fetchProBankAccList(res.data.project).then(() => message()))
      .catch(err => errorHandle(err.response.data))

  const deleteProBankAcc = (pk: number, project: number) =>
    api
      .delete(`/project-bank-account/${pk}/`)
      .then(() =>
        fetchProBankAccList(project).then(() =>
          message('danger', '알림!', '해당 오브젝트가 삭제되었습니다.'),
        ),
      )
      .catch(err => errorHandle(err.response.data))

  const balanceByAccList = ref<BalanceByAccount[]>([])

  const fetchBalanceByAccList = (payload: any) => {
    const { project, date } = payload
    let url = `/pr-balance-by-acc/?project=${project}`
    if (date) url += `&date=${date}`
    return api
      .get(url)
      .then(res => (balanceByAccList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proDateCashBook = ref<ProjectCashBook[]>([])

  const fetchDateCashBookList = (payload: any) => {
    const { project, date } = payload
    const url = `/pr-date-cashbook/?project=${project}&date=${date}`
    return api
      .get(url)
      .then(res => (proDateCashBook.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proBudgetList = ref<ProjectBudget[]>([])

  const fetchProjectBudgetList = (project: number) =>
    api
      .get(`/budget/?project=${project}`)
      .then(res => (proBudgetList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const execAmountList = ref<ExecAmountToBudget[]>([])

  const fetchExecAmountList = (project: number, date = '') =>
    api
      .get(`/exec-amount/?project=${project}&date=${date}`)
      .then(res => (execAmountList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))

  const proCashBookList = ref<ProjectCashBook[]>([])
  const getProCashLogs = computed(() =>
    proCashBookList.value
      ? proCashBookList.value.map((p: ProjectCashBook) => ({
          pk: p.pk,
          project: p.project,
          sort: p.sort,
          sort_desc: sortList.value
            ? sortList.value.filter(s => s.pk === p.sort).map(s => s.name)[0]
            : '-',
          project_account_d1:
            p.project_account_d1 === null ? '' : String(p.project_account_d1),
          project_account_d1_desc: p.project_account_d1
            ? allAccD1List.value
                .filter(d => d.pk === p.project_account_d1)
                .map(d => d.name)[0]
            : '-',
          project_account_d2:
            p.project_account_d2 === null ? '' : String(p.project_account_d2),
          project_account_d2_desc: p.project_account_d2
            ? allAccD2List.value
                .filter(d => d.pk === p.project_account_d2)
                .map(d => d.name)[0]
            : '-',
          content: p.content,
          trader: p.trader,
          bank_account: p.bank_account,
          bank_account_desc: proBankAccountList.value
            ? proBankAccountList.value
                .filter(b => b.pk === p.bank_account)
                .map(b => b.alias_name)[0]
            : '-',
          income: p.income,
          outlay: p.outlay,
          evidence: p.evidence,
          evidence_desc: p.evidence_desc,
          note: p.note,
          deal_date: p.deal_date,
          contract: p.contract,
          is_separate: p.is_separate,
          separated: p.separated,
          sepItems: p.sepItems,
        }))
      : [],
  )
  const proCashesCount = ref<number>(0)

  const fetchProjectCashList = (payload: any) => {
    const { project } = payload
    let url = `/project-cashbook/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.pro_acc_d1) url += `&project_account_d1=${payload.pro_acc_d1}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
    if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    return api
      .get(url)
      .then(res => (proCashBookList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proCashPages = (itemsPerPage: number) =>
    Math.ceil(proCashesCount.value / itemsPerPage)

  const proImprestList = ref<ProjectCashBook[]>([])
  const getProImprestLogs = computed(() =>
    proImprestList.value
      ? proImprestList.value.map((p: ProjectCashBook) => ({
          pk: p.pk,
          project: p.project,
          sort: p.sort,
          sort_desc: sortList.value
            ? sortList.value.filter(s => s.pk === p.sort).map(s => s.name)[0]
            : '-',
          project_account_d1:
            p.project_account_d1 === null ? '' : String(p.project_account_d1),
          project_account_d1_desc: p.project_account_d1
            ? allAccD1List.value
                .filter(d => d.pk === p.project_account_d1)
                .map(d => d.name)[0]
            : '-',
          project_account_d2:
            p.project_account_d2 === null ? '' : String(p.project_account_d2),
          project_account_d2_desc: p.project_account_d2
            ? allAccD2List.value
                .filter(d => d.pk === p.project_account_d2)
                .map(d => d.name)[0]
            : '-',
          content: p.content,
          trader: p.trader,
          bank_account: p.bank_account,
          bank_account_desc: proBankAccountList.value
            ? proBankAccountList.value
                .filter(b => b.pk === p.bank_account)
                .map(b => b.alias_name)[0]
            : '-',
          income: p.income,
          outlay: p.outlay,
          evidence: p.evidence,
          evidence_desc: p.evidence_desc,
          note: p.note,
          deal_date: p.deal_date,
          contract: p.contract,
          is_separate: p.is_separate,
          separated: p.separated,
          sepItems: p.sepItems,
        }))
      : [],
  )
  const proImprestCount = ref<number>(0)

  const fetchProjectImprestList = (payload: any) => {
    const { project } = payload
    let url = `/project-imprest/?project=${project}`
    if (payload.from_date) url += `&from_deal_date=${payload.from_date}`
    if (payload.to_date) url += `&to_deal_date=${payload.to_date}`
    if (payload.sort) url += `&sort=${payload.sort}`
    if (payload.pro_acc_d1) url += `&project_account_d1=${payload.pro_acc_d1}`
    if (payload.pro_acc_d2) url += `&project_account_d2=${payload.pro_acc_d2}`
    if (payload.bank_account) url += `&bank_account=${payload.bank_account}`
    if (payload.search) url += `&search=${payload.search}`
    const page = payload.page ? payload.page : 1
    if (payload.page) url += `&page=${page}`
    return api
      .get(url)
      .then(res => (proImprestList.value = res.data.results))
      .catch(err => errorHandle(err.response.data))
  }

  const proImprestPages = (itemsPerPage: number) =>
    Math.ceil(proImprestCount.value / itemsPerPage)

  const imprestBAccount = () =>
    proBankAccountList.value.filter(b => b.is_imprest)

  return {
    sortList,
    fetchProAccSortList,

    allAccD1List,
    fetchProAllAccD1List,

    allAccD2List,
    fetchProAllAccD2List,

    formAccD1List,
    fetchProFormAccD1List,

    formAccD2List,
    fetchProFormAccD2List,

    proBankAccountList,
    fetchProBankAccList,
    createProBankAcc,
    updateProBankAcc,
    deleteProBankAcc,

    balanceByAccList,
    fetchBalanceByAccList,

    proDateCashBook,
    fetchDateCashBookList,

    proBudgetList,
    fetchProjectBudgetList,

    execAmountList,
    fetchExecAmountList,

    proCashBookList,
    getProCashLogs,
    proCashesCount,
    fetchProjectCashList,
    proCashPages,

    proImprestList,
    getProImprestLogs,
    proImprestCount,
    fetchProjectImprestList,
    proImprestPages,
    imprestBAccount,
  }
})
