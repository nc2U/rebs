<template>
  <CRow class="p-2">
    <CCol md="4" class="mb-2">
      <CRow>
        <CFormLabel for="colFormLabel" class="col-sm-3 col-form-label">
          차수선택
        </CFormLabel>
        <CCol sm="9">
          <CFormSelect id="colFormLabel" placeholder="col-form-label">
          </CFormSelect>
        </CCol>
      </CRow>
    </CCol>

    <CCol md="4" class="mb-2">
      <CRow>
        <CFormLabel for="colFormLabel" class="col-sm-3 col-form-label">
          타입선택
        </CFormLabel>
        <CCol sm="9">
          <CFormSelect
            id="colFormLabel"
            placeholder="col-form-label"
          ></CFormSelect>
        </CCol>
      </CRow>
    </CCol>
  </CRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PriceSelectForm',
  props: ['selected'],
})
</script>
