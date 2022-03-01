<template>
  <CForm class="mt-3">
    <CRow class="mb-2">
      <CCol xs="6">
        <CRow>
          <CFormLabel color="dark" class="col-sm-4 col-form-label">
            수납일자
          </CFormLabel>
          <CCol sm="8">
            <DatePicker required placeholder="거래일자" />
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow class="mb-2">
      <CCol xs="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">납부회차</CFormLabel>
          <CCol sm="8">
            <CFormSelect>
              <option value="">---------</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol xs="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">수납금액</CFormLabel>
          <CCol sm="8">
            <CFormInput />
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow class="mb-2">
      <CCol xs="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">수납계좌</CFormLabel>
          <CCol sm="8">
            <CFormSelect>
              <option value="">---------</option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol xs="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">입금자명</CFormLabel>
          <CCol sm="8">
            <CFormInput />
          </CCol>
        </CRow>
      </CCol>
    </CRow>

    <CRow class="mb-2">
      <CCol>
        <CRow>
          <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
          <CCol sm="10">
            <CFormTextarea />
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CAlert color="secondary" class="text-right">
      <CButton color="primary">신규등록</CButton>
    </CAlert>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'

export default defineComponent({
  name: 'PayForm',
  components: { DatePicker },
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
