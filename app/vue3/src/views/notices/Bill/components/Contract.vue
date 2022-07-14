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
    get_price() {
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
  },
})
</script>
