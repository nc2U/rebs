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
        v-model.number="form.price_build"
        type="number"
        min="0"
        placeholder="타입별 건물가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_land"
        type="number"
        min="0"
        placeholder="타입별 대지가"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price_tax"
        type="number"
        min="0"
        placeholder="타입별 부가세"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput
        v-model.number="form.price"
        type="number"
        min="0"
        placeholder="타입별 공급가격"
      />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton
        :color="btn.color"
        size="sm"
        @click="onStorePrice"
        :disabled="formsCheck"
      >
        {{ btn.text }}
      </CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapGetters, mapState } from 'vuex'

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
      price: {},
      isData: false,
    }
  },
  props: ['floor', 'condTexts', 'queryIds'],
  computed: {
    btn() {
      const color = this.isData ? 'success' : 'primary'
      const text = this.isData ? '수정' : '등록'
      return { color, text }
    },
    formsCheck(this: any) {
      const a = this.form.price_build == this.price.price_build
      const b = this.form.price_land == this.price.price_land
      const c = this.form.price_tax == this.price.price_tax
      const d = this.form.price == this.price.price
      return (a && b && c && d) || !this.isData
    },
    ...mapState('cash', ['priceList']),
  },
  watch: {
    priceList() {
      const unit_floor_type = String(this.floor.pk)
      const { project, order_group, unit_type }: any = this.queryIds
      const price = this.priceList.filter(
        (p: any) =>
          p.project == project &&
          p.order_group == order_group &&
          p.unit_type == unit_type &&
          p.unit_floor_type == unit_floor_type,
      )[0]
      this.price = price
      this.isData = price ? true : false
      this.form.price_build = price ? price.price_build : null
      this.form.price_land = price ? price.price_land : null
      this.form.price_tax = price ? price.price_tax : null
      this.form.price = price ? price.price : null
    },
  },
  methods: {
    onStorePrice(this: any) {
      const payload = this.form
      if (!this.price) this.$emit('on-create', payload)
      else {
        const updatePayload = { ...{ pk: this.price.pk }, ...payload }
        this.$emit('on-update', updatePayload)
      }
    },
  },
})
</script>
