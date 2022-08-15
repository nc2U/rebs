<script lang="ts" setup>
import { ref, watch } from 'vue'

const props = defineProps({
  orders: { type: Object, default: null },
  types: { type: Object, default: null },
})
const emit = defineEmits(['on-order-select', 'on-type-select'])

const order = ref('')
const type = ref('')
const orderDisabled = ref(false)

watch(props, () => {
  order.value = ''
  type.value = ''
})

const onOrderSelect = (e: any) => {
  type.value = ''
  emit('on-order-select', e.target.value)
}
const onTypeSelect = (e: any) => emit('on-type-select', e.target.value)
</script>

<template>
  <CCallout color="warning" class="pb-2 mb-4">
    <CRow>
      <CCol md="4" class="mb-2">
        <CRow>
          <CFormLabel for="sel1" class="col-sm-3 col-form-label">
            차수선택
          </CFormLabel>
          <CCol sm="9">
            <CFormSelect
              id="sel1"
              v-model="order"
              :disabled="orderDisabled"
              @change="onOrderSelect"
            >
              <option value="">---------</option>
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
              :disabled="order == ''"
              @change="onTypeSelect"
            >
              <option value="">---------</option>
              <option v-for="type in types" :key="type.pk" :value="type.pk">
                {{ type.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
