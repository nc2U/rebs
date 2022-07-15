<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>
      <CFormCheck
        v-model="checked"
        :id="'check_' + contract.ctor_pk"
        :value="contract.ctor_pk"
        @change="ctorChk(contract.ctor_pk)"
        :disabled="paidCompleted"
        label="선택"
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
      <span v-if="paidCompleted" class="text-secondary">완납중</span>
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

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Contract',
  props: {
    contract: {
      type: Object,
      required: true,
    },
    page: Number,
    now_order: Number,
    allChecked: Boolean,
  },
  data() {
    return {
      checked: false,
      orderList: [{ pay_time: null }],
    }
  },
  computed: {
    paidCompleted() {
      const due: number = this.now_order || 2
      const paid: number = this.get_paid_order()
      return paid >= due
    },
    price() {
      // 해당 건별 분양가 구하기
      const c = this.contract
      const unit = c.house_unit
      return unit
        ? this.salesPriceList.filter(
            (s: any) =>
              s.order_group === c.order_group.pk &&
              s.unit_type === c.type_pk &&
              s.unit_floor_type === unit.floor_type,
          )[0]?.price
        : this.contract.average_price
    },

    downPay() {
      // 계약금 구하기
      const c = this.contract
      const pay_num = this.payOrderList.filter(
        (p: any) => p.pay_sort === '1',
      ).length
      const average_downPay = Number(
        (this.price * 0.1) / Math.round(pay_num / 2),
      )

      const downPay = this.downPaymentList.filter(
        (d: any) =>
          d.order_group === c.order_group.pk && d.unit_type === c.type_pk,
      )[0]

      return downPay ? downPay.payment_amount : average_downPay
    },
    lastPayName() {
      return this.payOrderList[this.payOrderList.length - 1].pay_time
    },
    ...mapState('payment', ['payOrderList']),
    ...mapState('contract', ['salesPriceList', 'downPaymentList']),
  },
  mounted() {
    this.orderList = this.payOrderList
  },
  watch: {
    allChecked(val) {
      if (!this.paidCompleted) {
        this.checked = val
        this.ctorChk(this.contract.ctor_pk)
      }
    },
    page(n, o) {
      if (n !== o) this.checked = false
    },
  },
  methods: {
    ctorChk(ctorPk: string) {
      this.$nextTick(() => {
        this.$emit('on-ctor-chk', { chk: this.checked, pk: ctorPk })
      })
    },

    get_paid_order() {
      let paid_amount = 0
      const total_paid = this.contract.total_paid
      let paid_orders: any[] = []

      const middle = Number(this.price * 0.1)

      this.orderList.forEach((p: any) => {
        if (p.pay_sort === '1') paid_amount += this.downPay
        else if (p.pay_sort === '2') paid_amount += middle

        if (total_paid >= paid_amount) {
          paid_orders.push(p.pay_time)
        }
      })
      return total_paid >= this.price ? this.lastPayName : paid_orders.pop()
    },
    getPayName(pay_time: number) {
      return this.payOrderList
        .filter((p: any) => p.pay_time === pay_time)
        .map((p: any) => p.pay_name)[0]
    },
  },
})
</script>
