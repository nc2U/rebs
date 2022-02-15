<template>
  <CCallout color="secondary">
    <CRow class="row g-3">
      <CCol md="9">
        <CRow>
          <CCol md="2">
            <CFormLabel for="inputEmail4">차수</CFormLabel>
            <CFormSelect id="inputState">
              <option>---------</option>
              <option>...</option>
            </CFormSelect>
          </CCol>
          <CCol md="2">
            <CFormLabel for="inputPassword4">타입</CFormLabel>
            <CFormSelect id="inputState">
              <option>---------</option>
              <option>...</option>
            </CFormSelect>
          </CCol>
          <CCol md="2">
            <CFormLabel for="inputPassword4">동별</CFormLabel>
            <CFormSelect id="inputState">
              <option>---------</option>
              <option>...</option>
            </CFormSelect>
          </CCol>
          <CCol md="2">
            <CFormLabel for="inputPassword4">상태</CFormLabel>
            <CFormSelect id="inputState">
              <option>---------</option>
              <option>...</option>
            </CFormSelect>
          </CCol>
          <CCol md="2" class="mb-3">
            <CFormLabel for="inptState">계약기간</CFormLabel>
            <CFormInput type="text" id="inputEmail4" />
          </CCol>
          <CCol md="2">
            <CFormLabel class="d-none d-md-block" for="inputZip">
              &nbsp;
            </CFormLabel>
            <CFormInput id="inputZip" />
          </CCol>
        </CRow>
      </CCol>
      <CCol md="3">
        <CFormLabel class="d-none d-md-block" for="inputZip">&nbsp;</CFormLabel>
        <CInputGroup class="flex-nowrap">
          <CFormInput
            placeholder="계약자, 일련번호, 비고"
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
