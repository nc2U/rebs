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
      {{ get_paid_order() }}
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.serial_number }}
      </router-link>
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
    <CTableDataCell
      class="text-left"
      :class="contract.house_unit.__str__ === '' ? 'text-danger' : ''"
    >
      {{ contract.house_unit.__str__ || '[미정]' }}
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.contractor }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_paid) }}
    </CTableDataCell>
    <CTableDataCell>
      {{ '완납중' }}
      ({{
        contract.last_paid_order === '-'
          ? '계약금미납'
          : contract.last_paid_order.pay_name
      }})
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
    }
  },
  computed: {
    paidCompleted() {
      const due: number = this.now_order || 2
      const paid: number = this.contract.last_paid_order.pay_time
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
      const ad = Number((this.price * 0.1) / Math.round(pay_num / 2))

      return (
        this.downPaymentList.filter(
          (d: any) =>
            d.order_group === c.order_group.pk && d.unit_type === c.type_pk,
        )[0].payment_amount || ''
      )
    },
    ...mapState('payment', ['payOrderList']),
    ...mapState('contract', ['salesPriceList', 'downPaymentList']),
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
      // const middle = Number(price * 0.1)
      // const bal_order_num = this.payOrderList.filter(
      //   (p: any) => p.pay_sort === '3',
      // ).length
      // const balance = Number(this.get_price() - paid_amount) / bal_order_num
      let paid_orders: any[] = []
      const total_paid = this.contract.total_paid

      this.payOrderList.forEach((p: any) => {
        // if (p.pay_sort === '1') paid_amount += this.downPay
        //   // else if (p.pay_sort === '2') paid_amount += middle
        //   //   //   else paid_amount += balance
        //   //   //
        if (total_paid >= paid_amount) {
          paid_orders.push(p.pay_time)
        }
      })
      return paid_orders
    },
  },
})
</script>
