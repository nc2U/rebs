<template>
  <CTableRow>
    <CTableDataCell class="text-center">
      {{ condTexts.orderText }}
    </CTableDataCell>
    <CTableDataCell class="text-center">
      {{ condTexts.typeText }}
    </CTableDataCell>
    <CTableDataCell> {{ floor.alias_name }}</CTableDataCell>

    <CTableDataCell>
      <CFormInput
        v-model="form.price_build"
        type="number"
        min="0"
        placeholder="타입별 건물가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.price_land"
        type="number"
        min="0"
        placeholder="타입별 대지가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.price_tax"
        type="number"
        min="0"
        placeholder="타입별 부가세"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model="form.price"
        type="number"
        min="0"
        placeholder="타입별 공급가격"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton color="success" size="sm">저장</CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'Price',
  data() {
    return {
      form: {
        price_build: null,
        price_land: null,
        price_tax: null,
        price: null,
      },
    }
  },
  created(this: any) {
    this.priceRefresh()
  },
  props: ['floor', 'condTexts', 'queryIds'],
  computed: {
    ...mapState('cash', ['priceList']),
  },
  methods: {
    priceRefresh(this: any) {
      const floorId = String(this.floor.pk)
      const { projId, orderId, typeId }: any = this.queryIds
      const price = this.priceList.filter(
        (p: any) =>
          p.project == projId &&
          p.order_group == orderId &&
          p.unit_type == typeId &&
          p.unit_floor_type == floorId,
      )[0]
      this.form.price_build = price ? price.price_build : null
      this.form.price_land = price ? price.price_land : null
      this.form.price_tax = price ? price.price_tax : null
      this.form.price = price ? price.price : null
    },
  },
})
</script>
