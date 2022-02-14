<template>
  <CCallout color="secondary">
    <CRow class="row g-3">
      <CCol md="2">
        <CFormLabel for="inputEmail4">차수</CFormLabel>
        <CFormInput type="text" id="inputEmail4" />
      </CCol>
      <CCol md="2">
        <CFormLabel for="inputPassword4">타입</CFormLabel>
        <CFormInput id="inputCity" />
      </CCol>
      <CCol md="2">
        <CFormLabel for="inputCity">정렬순서</CFormLabel>
        <CFormSelect id="inputState">
          <option>Choose...</option>
          <option>...</option>
        </CFormSelect>
      </CCol>
      <CCol md="2">
        <CFormLabel for="inputState">계약기간</CFormLabel>
        <CFormInput type="text" id="inputEmail4" />
      </CCol>
      <CCol md="2">
        <CFormLabel for="inputZip">&nbsp;</CFormLabel>
        <CFormInput id="inputZip" />
      </CCol>
      <CCol md="2">
        <CFormLabel for="inputZip">&nbsp;</CFormLabel>
        <CInputGroup class="flex-nowrap">
          <CFormInput
            placeholder="Username"
            aria-label="Username"
            aria-describedby="addon-wrapping"
          />
          <CInputGroupText id="addon-wrapping">검색</CInputGroupText>
        </CInputGroup>
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ListController',
  components: {},
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {},
  methods: {},
})
</script>
