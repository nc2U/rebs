<script lang="ts" setup>
import { ref, computed } from 'vue'
import { pageTitle, navMenu } from '@/views/payments/_menu/headermixin'
import { useProject } from '@/store/pinia/project'
import ContentHeader from '@/layouts/ContentHeader/Index.vue'
import ContentBody from '@/layouts/ContentBody/Index.vue'
import DateChoicer from '@/views/payments/Status/components/DateChoicer.vue'
import TableTitleRow from '@/components/TableTitleRow.vue'
import PaymentStatus from './components/PaymentStatus.vue'

const date = ref(new Date())

const projectStore = useProject()
const initProjId = computed(() => projectStore.initProjId)
const project = computed(() => projectStore.project?.pk || initProjId.value)

const excelUrl = computed(() => {
  let url = ''
  return url
})

// const onSelectAdd = (target: number) => {
//   if (!!target) {
//     fetchProBankAccList(target)
//     fetchBalanceByAccList({ project: target, date: dateFormat(date.value) })
//     fetchDateCashBookList({
//       project: target,
//       date: dateFormat(date.value),
//     })
//     fetchProjectBudgetList(target)
//     fetchExecAmountList(target, dateFormat(date.value))
//   } else {
//     proCashStore.proBankAccountList = []
//     proCashStore.balanceByAccList = []
//     proCashStore.proDateCashBook = []
//     proCashStore.proBudgetList = []
//     proCashStore.execAmountList = []
//   }
// }
const setDate = (date: Date) => date
</script>

<template>
  <ContentHeader :page-title="pageTitle" :nav-menu="navMenu" />

  <ContentBody>
    <CCardBody class="pb-5">
      <DateChoicer @set-date="setDate" />

      <TableTitleRow excel :url="excelUrl" :disabled="true" />
      <PaymentStatus :date="date" />
    </CCardBody>

    <CCardFooter>&nbsp;</CCardFooter>
  </ContentBody>
</template>
