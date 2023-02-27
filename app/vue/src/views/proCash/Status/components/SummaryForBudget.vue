<script lang="ts" setup>
import { computed, onBeforeMount, ref, watch } from 'vue'
import { useProject } from '@/store/pinia/project'
import { write_project_cash } from '@/utils/pageAuth'
import { dateFormat, numFormat } from '@/utils/baseMixins'
import { TableInfo, TableSecondary } from '@/utils/cssMixins'
import {
  ProOutBudget,
  ExecAmountToBudget as ExeBudget,
} from '@/store/types/project'

defineProps({ date: { type: String, default: '' } })

const formNumber = ref(1000)

const totalBudget = ref(0)
const preExecAmt = ref(0)
const monthExecAmt = ref(0)
const totalExecAmt = ref(0)
const availableBudget = ref(0)

const projectStore = useProject()
const proOutBudgetList = computed(() => projectStore.proOutBudgetList)
const execAmountList = computed(() => projectStore.execAmountList)

onBeforeMount(() => getSumTotal())

watch(proOutBudgetList, () => getSumTotal())

const getD2sInter = (arr: number[]) => {
  const d2s = proOutBudgetList.value.map((b: ProOutBudget) => b.account_d2.pk)
  return arr.filter(x => d2s.includes(x))
}
const getLength = (arr: number[]) => getD2sInter(arr).length

const getFirst = (arr: number[]) => getD2sInter(arr)[0]

const getSubTitle = (sub: string) =>
  sub !== ''
    ? proOutBudgetList.value
        .filter((b: ProOutBudget) => b.account_d2.sub_title === sub)
        .map((b: ProOutBudget) => b.pk)
    : []

const getExecAmount = (d2: number) =>
  execAmountList.value.filter((e: ExeBudget) => e.acc_d2 === d2)

const getEASum = (d2: number) =>
  getExecAmount(d2).map((e: ExeBudget) => e.all_sum)[0]

const getEAMonth = (d2: number) =>
  getExecAmount(d2).map((e: ExeBudget) => e.month_sum)[0]

const getSumTotal = () => {
  const totalBudgetCalc = proOutBudgetList.value
    .map((b: ProOutBudget) => b.budget)
    .reduce((res: number, val: number) => res + val, 0)
  const monthExecAmtCalc = execAmountList.value
    .map((a: ExeBudget) => a.month_sum)
    .reduce((r: number, v: number) => r + v, 0)
  const totalExecAmtCalc = execAmountList.value
    .map((a: ExeBudget) => a.all_sum)
    .reduce((r: number, v: number) => r + v, 0)

  totalBudget.value = totalBudgetCalc
  preExecAmt.value = totalExecAmtCalc - monthExecAmtCalc
  monthExecAmt.value = monthExecAmtCalc
  totalExecAmt.value = totalExecAmtCalc
  availableBudget.value = totalBudgetCalc - totalExecAmtCalc
}

const emit = defineEmits(['patch-budget'])

const patchBudget = (pk: number, budget: string, oldBudget: number) => {
  formNumber.value = 1000
  if (write_project_cash.value) {
    const bg = parseInt(budget)
    if (bg !== oldBudget) emit('patch-budget', pk, bg)
  } else {
    alert('예산수정 권한없음!')
  }
}
</script>

<template>
  <CTable hover responsive bordered align="middle">
    <colgroup>
      <col width="5%" />
      <col width="5%" />
      <col width="10%" />
      <col width="10%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
      <col width="14%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="8">
          <strong>
            <CIcon name="cilFolderOpen" />
            사업예산 및 집행현황
          </strong>
          <small class="text-medium-emphasis">
            ({{ dateFormat(date) }}) 기준
          </small>
        </CTableDataCell>
        <CTableDataCell class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell colspan="4">구분</CTableHeaderCell>
        <CTableHeaderCell>예산액</CTableHeaderCell>
        <CTableHeaderCell>전월 집행금액 누계</CTableHeaderCell>
        <CTableHeaderCell>당월 집행금액</CTableHeaderCell>
        <CTableHeaderCell>집행금액 합계</CTableHeaderCell>
        <CTableHeaderCell>가용(잔여) 예산합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow
        v-for="(bdj, i) in proOutBudgetList"
        :key="bdj.pk"
        class="text-right"
      >
        <CTableDataCell
          v-if="i === 0"
          :color="TableInfo"
          class="text-center"
          :rowspan="proOutBudgetList.length"
        >
          사업비
        </CTableDataCell>
        <CTableDataCell
          v-if="getFirst(bdj.account_d1.acc_d2s) === bdj.account_d2.pk"
          class="text-center"
          :rowspan="getLength(bdj.account_d1.acc_d2s)"
        >
          {{ bdj.account_d1.name }}
        </CTableDataCell>
        <CTableDataCell
          v-if="
            bdj.account_d2.sub_title &&
            bdj.pk === getSubTitle(bdj.account_d2.sub_title)[0]
          "
          class="text-left"
          :rowspan="getSubTitle(bdj.account_d2.sub_title).length"
        >
          {{ bdj.account_d2.sub_title }}
        </CTableDataCell>
        <CTableDataCell
          class="text-left"
          :colspan="bdj.account_d2.sub_title ? 1 : 2"
        >
          {{ bdj.account_d2.name }}
        </CTableDataCell>
        <CTableDataCell
          class="py-0 bg-blue-grey-lighten-5"
          style="cursor: pointer"
          @dblclick="formNumber = i"
        >
          <span v-if="formNumber !== i">
            {{ numFormat(bdj.budget) }}
          </span>
          <span v-else class="p-0">
            <CFormInput
              type="text"
              class="form-control text-right"
              size="sm"
              :value="bdj.budget"
              @blur="patchBudget(bdj.pk, $event.target.value, bdj.budget)"
              @keydown.enter="
                patchBudget(bdj.pk, $event.target.value, bdj.budget)
              "
            />
          </span>
        </CTableDataCell>
        <CTableDataCell>
          {{
            numFormat(
              getEASum(bdj.account_d2.pk) - getEAMonth(bdj.account_d2.pk),
            )
          }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEAMonth(bdj.account_d2.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEASum(bdj.account_d2.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell
          :class="bdj.budget < getEASum(bdj.account_d2.pk) ? 'text-danger' : ''"
        >
          {{ numFormat(bdj.budget - (getEASum(bdj.account_d2.pk) || 0)) }}
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-right">
        <CTableHeaderCell colspan="4" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totalBudget) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(preExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(monthExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(totalExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(availableBudget) }}</CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
