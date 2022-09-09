<script lang="ts" setup>
import { ref, watch } from 'vue'

const props = defineProps({
  orders: { type: Object, default: null },
  types: { type: Object, default: null },
})
const emit = defineEmits(['on-order-select', 'on-type-select'])

const order = ref<number | null>(null)
const type = ref<number | null>(null)

watch(props, () => {
  order.value = null
  type.value = null
})

const onOrderSelect = (e: Event) => {
  type.value = null
  emit('on-order-select', (e.target as HTMLSelectElement).value)
}
const onTypeSelect = (e: Event) =>
  emit('on-type-select', (e.target as HTMLSelectElement).value)
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
            <CFormSelect id="sel1" v-model="order" @change="onOrderSelect">
              <option value="">---------</option>
              <option v-for="o in orders" :key="o.pk" :value="o.pk">
                {{ o.order_group_name }}
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
              :disabled="!order"
              @change="onTypeSelect"
            >
              <option value="">---------</option>
              <option v-for="t in types" :key="t.pk" :value="t.pk">
                {{ t.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
  </CCallout>
</template>
