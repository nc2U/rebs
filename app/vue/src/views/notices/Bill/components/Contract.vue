<script lang="ts" setup>
import { computed, ref, nextTick, watch } from 'vue'
import { usePayment } from '@/store/pinia/payment'
import { useContract } from '@/store/pinia/contract'
import { numFormat } from '@/utils/baseMixins'

const props = defineProps({
  contract: {
    type: Object,
    required: true,
  },
  page: { type: Number, default: 1 },
  nowOrder: { type: Number, default: null },
  allChecked: Boolean,
})

const emit = defineEmits(['on-ctor-chk'])

const checked = ref(false)
// const orderList = ref([{ pay_time: null }])

const paymentStore = usePayment()
const payOrderList = computed(() => paymentStore.payOrderList)

const contractStore = useContract()
const salesPriceList = computed(() => contractStore.salesPriceList)
const downPaymentList = computed(() => contractStore.downPaymentList)

const paidCompleted = computed(() => {
  const due: number = props.nowOrder || 2
  const paid: number = get_paid_order()
  return paid >= due
})
const price = computed(() => {
  // 해당 건별 분양가 구하기
  const c = props.contract
  const unit = c.house_unit
  return unit
    ? salesPriceList.value.filter(
        (s: any) =>
          s.order_group === c.order_group.pk &&
          s.unit_type === c.type_pk &&
          s.unit_floor_type === unit.floor_type,
      )[0]?.price
    : props.contract.average_price
})

const downPay = computed(() => {
  // 계약금 구하기
  const c = props.contract
  const pay_num = payOrderList.value.filter(
    (p: any) => p.pay_sort === '1',
  ).length
  const average_downPay = Number((price.value * 0.1) / Math.round(pay_num / 2))

  const downPay = downPaymentList.value.filter(
    (d: any) => d.order_group === c.order_group.pk && d.unit_type === c.type_pk,
  )[0]

  return downPay ? downPay.payment_amount : average_downPay
})
const lastPayName = computed(
  () => payOrderList.value[payOrderList.value.length - 1].pay_time,
)

watch(props, (n, o) => {
  if (!paidCompleted.value) {
    checked.value = n.allChecked
    ctorChk(n.contract.ctor_pk)
  }
  if (n.page !== o.page) checked.value = false
})
// watch: {
//   allChecked(val) {
//     if (!this.paidCompleted) {
//       this.checked = val
//       this.ctorChk(this.contract.ctor_pk)
//     }
//   },
//   page(n, o) {
//     if (n !== o) this.checked = false
//   },
// },

// onMounted(() => (orderList.value = payOrderList.value))

const ctorChk = (ctorPk: string) =>
  nextTick(() => {
    emit('on-ctor-chk', { chk: checked.value, pk: ctorPk })
  })

const get_paid_order = () => {
  let paid_amount = 0 // 금회차까지 납부해야할 금액 누계
  const total_paid = props.contract.total_paid // 총 낸돈
  let paid_orders: any[] = [] // 완납 회차 리스트

  const middle = Number(price.value * 0.1) // 중도금액

  payOrderList.value.forEach((p: any) => {
    if (p.pay_sort === '1') paid_amount += downPay.value // 계약금 더하기
    else if (p.pay_sort === '2') paid_amount += middle // 중도금 더하기

    if (total_paid >= paid_amount) paid_orders.push(p.pay_time) // (총 낸돈 >= 총 낼돈)
  })
  return price.value // total_paid >= price.value ? lastPayName.value : paid_orders.pop()
}

const getPayName = (pay_time: number) => {
  return payOrderList.value
    .filter((p: any) => p.pay_time === pay_time)
    .map((p: any) => p.pay_name)[0]
}
</script>

<template>
  <CTableRow
    v-if="contract"
    class="text-center"
    :color="checked ? 'secondary' : ''"
  >
    <CTableDataCell>
      <CFormCheck
        :id="'check_' + contract.ctor_pk"
        v-model="checked"
        :value="contract.ctor_pk"
        :disabled="paidCompleted"
        label="선택"
        @change="ctorChk(contract.ctor_pk)"
      />
    </CTableDataCell>
    <CTableDataCell>{{ contract.order_group.order_group_name }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CIcon
        name="cibDiscover"
        :style="'color:' + contract.type_color"
        size="sm"
        class="mr-1"
      />
      {{ contract.unit_type }}
    </CTableDataCell>
    <CTableDataCell>
      {{ contract.serial_number }}
    </CTableDataCell>
    <CTableDataCell
      class="text-center"
      :class="contract.house_unit_str ? '' : 'text-danger'"
    >
      {{ contract.house_unit_str || '미정' }}
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.contractor }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link
        :to="{ name: '건별수납 관리', query: { contract: contract.pk } }"
      >
        {{ numFormat(contract.total_paid) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      <span v-if="paidCompleted" class="text-success">완납중</span>
      <span v-else class="text-danger">미납중</span>
      {{
        contract.last_paid_order === '-'
          ? ' (계약금미납)'
          : ' (' + getPayName(get_paid_order()) + ')'
      }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
  </CTableRow>
</template>
