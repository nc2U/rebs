<script lang="ts" setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { dateFormat } from '@/utils/baseMixins'
import { headerSecondary } from '@/utils/cssMixins'
import Order from '@/views/payments/Register/components/Order.vue'

const props = defineProps({
  contract: { type: Object, default: null },
  paymentList: { type: Array, default: [] },
})

const store = useStore()

const payOrderList = computed(() => store.state.payment.payOrderList)
const priceList = computed(() => store.state.payment.priceList)
const downPayList = computed(() => store.state.payment.downPayList)

const thisPrice = computed(() => {
  if (props.contract) {
    return props.contract.keyunit.houseunit
      ? priceList.value
          .filter(
            (p: any) =>
              p.unit_floor_type === props.contract.keyunit.houseunit.floor_type,
          )
          .map((p: any) => p.price)[0]
      : Math.ceil(props.contract.unit_type.average_price / 10000) * 10000
  }
  return 0
})
const numDown = computed(
  () => payOrderList.value.filter((o: any) => o.pay_sort === '1').length,
)
const numMid = computed(
  () => payOrderList.value.filter((o: any) => o.pay_sort === '2').length,
)
const paidTotal = computed(() => {
  const paid = props.paymentList.map((p: any) => p.income)
  return paid.length === 0 ? 0 : paid.reduce((x: number, y: number) => x + y)
})
const dueTotal = computed(() => {
  let commitment: number[] = []
  const today = dateFormat(new Date())
  const dueOrder = payOrderList.value
    .filter(
      (o: any) =>
        (o.pay_due_date <= today && !o.extra_due_date) ||
        o.extra_due_date <= today,
    )
    .map((o: any) => o.pay_time)
  dueOrder.forEach((el: number) => {
    commitment.push(getCommits(el))
  })
  return commitment.length !== 0 ? commitment.reduce((x, y) => x + y) : 0
})

const commit = (pay_tyme: number) => getCommits(pay_tyme)

const getCommits = (el: number) => {
  const down = downPayList.value
    .filter((d: any) => d.order_group === props.contract.order_group.pk)
    .filter((d: any) => d.unit_type === props.contract.unit_type.pk)
    .map((d: any) => d.payment_amount)[0] // 1. downPayList, 2. payByOrder, 3. 분양가 / 총회차수

  const order = payOrderList.value.find((o: any) => o.pay_time === el)

  const payByOrder = order.pay_ratio
    ? thisPrice.value * order.pay_ratio
    : thisPrice.value * 0.1 // 1. payByOrder === '중도금' (지정된 비율이 없으면 회당 10%)
  const downPay = down ? down : payByOrder
  const balace =
    thisPrice.value - downPay * numDown.value - payByOrder * numMid.value // 분양가 - (계약금 + 중도금), 2. payByOrder
  const balacePay = balace ? balace : payByOrder * order.pay_ratio

  if (order.pay_sort === '1') {
    return downPay // 계약금
  } else if (order.pay_sort === '2') {
    return payByOrder // 중도금
  } else if (order.pay_sort === '3') {
    return balacePay // 잔금
  } else return 0
}
</script>

<template>
  <CTable hover responsive>
    <colgroup>
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
    </colgroup>

    <CTableHead :color="headerSecondary" class="text-center">
      <CTableRow>
        <CTableHeaderCell>납부기일</CTableHeaderCell>
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>약정금액</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>미(과오)납</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <CTableRow v-for="po in payOrderList" :key="po.pk" class="text-right">
        <Order
          :contract="contract"
          :price="thisPrice"
          :order="po"
          :commit="commit(po.pay_time)"
          :num-down="numDown"
          :num-mid="numMid"
          :payment-list="paymentList"
        />
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell :color="headerSecondary" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(thisPrice || 0) }}</CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(paidTotal) }}</CTableHeaderCell>
        <CTableHeaderCell
          :class="paidTotal - dueTotal < 0 ? 'text-danger' : ''"
        >
          {{ numFormat(paidTotal - dueTotal) }}
        </CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>
