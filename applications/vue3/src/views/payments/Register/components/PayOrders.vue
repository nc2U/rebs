<template>
  <CTable hover responsive>
    <colgroup>
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
      <col width="20%" />
    </colgroup>

    <CTableHead color="dark" class="text-center">
      <CTableRow>
        <CTableHeaderCell>납부기일</CTableHeaderCell>
        <CTableHeaderCell>구분</CTableHeaderCell>
        <CTableHeaderCell>약정금액</CTableHeaderCell>
        <CTableHeaderCell>수납금액</CTableHeaderCell>
        <CTableHeaderCell>미(과오)납</CTableHeaderCell>
      </CTableRow>
    </CTableHead>

    <CTableBody v-if="contract">
      <CTableRow class="text-right" v-for="po in payOrderList" :key="po.pk">
        <Order
          :contract="contract"
          :price="thisPrice"
          :order="po"
          :num-down="numDown"
          :num-mid="numMid"
        />
      </CTableRow>
    </CTableBody>

    <CTableHead>
      <CTableRow class="text-right">
        <CTableHeaderCell color="dark" class="text-center">
          합계
        </CTableHeaderCell>
        <CTableHeaderCell></CTableHeaderCell>
        <CTableHeaderCell>{{ numFormat(thisPrice || 0) }}</CTableHeaderCell>
        <CTableHeaderCell>실납부총액</CTableHeaderCell>
        <CTableHeaderCell>현재까지미과오납</CTableHeaderCell>
      </CTableRow>
    </CTableHead>
  </CTable>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Order from '@/views/payments/Register/components/Order.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'PayOrders',
  components: { Order },

  props: { contract: Object },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    thisPrice(this: any) {
      if (this.contract) {
        return this.contract.keyunit.houseunit
          ? this.priceList
              .filter(
                (p: any) =>
                  p.unit_floor_type ===
                  this.contract.keyunit.houseunit.floor_type,
              )
              .map((p: any) => p.price)[0]
          : this.contract.unit_type.average_price
      }
      return 0
    },
    numDown() {
      return this.payOrderList.filter((o: any) => o.pay_sort === '1').length
    },
    numMid() {
      return this.payOrderList.filter((o: any) => o.pay_sort === '2').length
    },
    ...mapState('payment', ['payOrderList', 'priceList']),
  },
  methods: {},
})
</script>
