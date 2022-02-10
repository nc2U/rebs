<template>
  <CRow class="p-2">
    <CCol md="4" class="mb-2">
      <CRow>
        <CFormLabel for="sel1" class="col-sm-3 col-form-label">
          차수선택
        </CFormLabel>
        <CCol sm="9">
          <CFormSelect
            id="sel1"
            ref="order"
            v-model="order"
            @change="onOrderSelect"
          >
            <option value="">차수 선택</option>
            <option v-for="order in orders" :key="order.pk" :value="order.pk">
              {{ order.order_group_name }}
            </option>
          </CFormSelect>
        </CCol>
      </CRow>
    </CCol>

    <CCol md="4" class="mb-2">
      <CRow>
        <CFormLabel for="sel2" class="col-sm-3 col-form-label">
          타입선택
        </CFormLabel>
        <CCol sm="9">
          <CFormSelect
            id="sel2"
            v-model="type"
            @change="onTypeSelect"
            :disabled="order == ''"
          >
            <option value="">타입 선택</option>
            <option v-for="type in types" :key="type.pk" :value="type.pk">
              {{ type.name }}
            </option>
          </CFormSelect>
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PriceSelectForm',
  data() {
    return {
      order: '',
      type: '',
    }
  },
  props: ['selected', 'orders', 'types'],
  methods: {
    onOrderSelect(e: any) {
      this.type = ''
      this.$emit('on-order-select', e.target.value)
    },
    onTypeSelect(e: any) {
      this.$emit('on-type-select', e.target.value)
    },
  },
})
</script>
