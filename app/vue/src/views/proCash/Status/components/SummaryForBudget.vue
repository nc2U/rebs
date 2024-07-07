<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useProject } from '@/store/pinia/project'
import { write_project_cash } from '@/utils/pageAuth'
import { numFormat } from '@/utils/baseMixins'
import { TableInfo, TableSecondary } from '@/utils/cssMixins'
import { type StatusOutBudget, type ExecAmountToBudget as ExeBudget } from '@/store/types/project'

defineProps({ date: { type: String, default: '' } })

const formNumber = ref(1000)
const isRevised = ref(1)

const projStore = useProject()
const execAmountList = computed(() => projStore.execAmountList)
const statusOutBudgetList = computed(() => projStore.statusOutBudgetList)

const getD3sInter = (arr: number[]) => {
  const d3s = statusOutBudgetList.value.map((b: StatusOutBudget) => b.account_d3.pk)
  return arr.filter(x => d3s.includes(x))
}
const getLength = (arr: number[]) => getD3sInter(arr).length

const isFirst = (arr: number[], d3Pk: number) => getD3sInter(arr)[0] === d3Pk

const getSubTitle = (sub: string, d2: number) =>
  sub !== ''
    ? statusOutBudgetList.value
        .filter((b: StatusOutBudget) => b.account_opt === sub && b.account_d2.pk === d2)
        .map(b => b.pk)
    : []

const getExecAmount = (d3: number) => execAmountList.value.filter((e: ExeBudget) => e.acc_d3 === d3)

const getEASum = (d3: number) => getExecAmount(d3).map((e: ExeBudget) => e.all_sum)[0]

const getEAMonth = (d3: number) => getExecAmount(d3).map((e: ExeBudget) => e.month_sum)[0]

const sumTotal = computed(() => {
  const totalBudgetCalc = statusOutBudgetList.value
    .map((b: StatusOutBudget) => b.budget)
    .reduce((res: number, val: number) => res + val, 0)
  const monthExecAmtCalc = execAmountList.value
    .map((a: ExeBudget) => a.month_sum)
    .reduce((r: number, v: number) => r + v, 0)
  const totalExecAmtCalc = execAmountList.value
    .map((a: ExeBudget) => a.all_sum)
    .reduce((r: number, v: number) => r + v, 0)

  const totalBudget = totalBudgetCalc
  const preExecAmt = totalExecAmtCalc - monthExecAmtCalc
  const monthExecAmt = monthExecAmtCalc
  const totalExecAmt = totalExecAmtCalc
  const availableBudget = totalBudgetCalc - totalExecAmtCalc
  return {
    totalBudget,
    preExecAmt,
    monthExecAmt,
    totalExecAmt,
    availableBudget,
  }
})

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
      <col style="width: 5%" />
      <col style="width: 5%" />
      <col style="width: 10%" />
      <col style="width: 10%" />
      <col style="width: 14%" />
      <col style="width: 14%" />
      <col style="width: 14%" />
      <col style="width: 14%" />
      <col style="width: 14%" />
    </colgroup>
    <CTableHead>
      <CTableRow>
        <CTableDataCell colspan="4">
          <strong>
            <CIcon name="cilFolderOpen" />
            사업예산 및 집행현황
          </strong>
          <small class="text-medium-emphasis"> ({{ date }}) 기준 </small>
        </CTableDataCell>
        <CTableDataCell class="text-center bg-yellow-lighten-5">
          <v-radio-group
            v-model="isRevised"
            inline
            size="sm"
            density="compact"
            hide-details
            style="font-size: 0.8em"
          >
            <img src="" />

            <p>
              <img src="" alt="" />
            </p>

            <v-radio label="기초 예산" :value="0" />
            <v-radio label="현황 예산" :value="1" />
          </v-radio-group>
        </CTableDataCell>
        <CTableDataCell colspan="4" class="text-right">(단위: 원)</CTableDataCell>
      </CTableRow>
      <CTableRow :color="TableSecondary" class="text-center">
        <CTableHeaderCell colspan="4">구분</CTableHeaderCell>
        <CTableHeaderCell color="dark" v-show="!isRevised">기초 예산액</CTableHeaderCell>
        <CTableHeaderCell v-show="isRevised">현황 예산액</CTableHeaderCell>
        <CTableHeaderCell>전월 집행금액 누계</CTableHeaderCell>
        <CTableHeaderCell>당월 집행금액</CTableHeaderCell>
        <CTableHeaderCell>집행금액 합계</CTableHeaderCell>
        <CTableHeaderCell>가용(잔여) 예산합계</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody>
      <CTableRow v-for="(obj, i) in statusOutBudgetList" :key="obj.pk" class="text-right">
        <CTableDataCell
          v-if="i === 0"
          :color="TableInfo"
          class="text-center"
          :rowspan="statusOutBudgetList.length"
        >
          사업비
        </CTableDataCell>
        <CTableDataCell
          v-if="isFirst(obj.account_d2.pro_d3s, obj.account_d3.pk)"
          class="text-center"
          :rowspan="getLength(obj.account_d2.pro_d3s)"
        >
          {{ obj.account_d2.name }}
        </CTableDataCell>
        <CTableDataCell
          v-if="obj.account_opt && obj.pk === getSubTitle(obj.account_opt, obj.account_d2.pk)[0]"
          class="text-left"
          :rowspan="getSubTitle(obj.account_opt, obj.account_d2.pk).length"
        >
          {{ obj.account_opt }}
        </CTableDataCell>
        <CTableDataCell class="text-left" :colspan="obj.account_opt ? 1 : 2">
          {{ obj.account_d3.name }}
          <v-tooltip v-if="obj.basis_calc" activator="parent" location="right">
            {{ obj.basis_calc }}
          </v-tooltip>
        </CTableDataCell>
        <CTableDataCell
          v-show="!isRevised"
          class="py-0 bg-blue-grey-lighten-4"
          style="cursor: pointer"
          @dblclick="formNumber = i"
        >
          <span v-if="formNumber !== i">
            {{ numFormat(obj.budget) }}
          </span>
          <span v-else class="p-0">
            <CFormInput
              type="text"
              class="form-control text-right"
              :value="obj.budget"
              @blur="patchBudget(obj.pk as number, $event.target.value, obj.budget)"
              @keydown.enter="patchBudget(obj.pk as number, $event.target.value, obj.budget)"
            />
          </span>
          <v-tooltip v-if="obj.basis_calc" activator="parent" location="left">
            {{ obj.basis_calc }}
          </v-tooltip>
        </CTableDataCell>
        <CTableDataCell
          v-show="isRevised"
          class="py-0 bg-blue-grey-lighten-5"
          style="cursor: pointer"
          @dblclick="formNumber = i"
        >
          <span v-if="formNumber !== i">
            {{ numFormat(obj.budget) }}
          </span>
          <span v-else class="p-0">
            <CFormInput
              type="text"
              class="form-control text-right"
              :value="obj.budget"
              @blur="patchBudget(obj.pk as number, $event.target.value, obj.budget)"
              @keydown.enter="patchBudget(obj.pk as number, $event.target.value, obj.budget)"
            />
          </span>
          <v-tooltip v-if="obj.basis_calc" activator="parent" location="left">
            {{ obj.basis_calc }}
          </v-tooltip>
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEASum(obj.account_d3.pk) - getEAMonth(obj.account_d3.pk)) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEAMonth(obj.account_d3.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell>
          {{ numFormat(getEASum(obj.account_d3.pk) || 0) }}
        </CTableDataCell>
        <CTableDataCell
          v-show="!isRevised"
          :class="obj.budget < getEASum(obj.account_d3.pk) ? 'text-danger' : ''"
        >
          {{ numFormat(obj.budget - (getEASum(obj.account_d3.pk) || 0)) }}
        </CTableDataCell>
        <CTableDataCell
          v-show="isRevised"
          :class="obj.budget < getEASum(obj.account_d3.pk) ? 'text-danger' : ''"
        >
          {{ numFormat(obj.budget - (getEASum(obj.account_d3.pk) || 0)) }}
        </CTableDataCell>
      </CTableRow>

      <CTableRow :color="TableSecondary" class="text-right">
        <CTableHeaderCell colspan="4" class="text-center"> 합계</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(sumTotal.totalBudget) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(sumTotal.preExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(sumTotal.monthExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(sumTotal.totalExecAmt) }}</CTableHeaderCell>
        <CTableHeaderCell v-show="!isRevised">
          {{ numFormat(sumTotal.availableBudget) }}
        </CTableHeaderCell>
        <CTableHeaderCell v-show="isRevised">
          {{ numFormat(sumTotal.availableBudget) }}
        </CTableHeaderCell>
      </CTableRow>
    </CTableBody>
  </CTable>
</template>
