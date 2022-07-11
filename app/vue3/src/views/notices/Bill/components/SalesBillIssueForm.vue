<template>
  <CAlert color="info">
    <CRow>
      <CCol xs="5" sm="6" md="7" lg="9">
        <CIcon name="cil-library-add" />
        <strong class="title"> 수납 고지서 발행</strong>
      </CCol>
      <CCol>
        <CFormSwitch
          label="고지서 관련정보 설정"
          :model-value="visible"
          @click="visible = !visible"
          id="formSwitch"
        />
      </CCol>
    </CRow>
  </CAlert>

  <CRow class="mb-1">
    <CCol sm="4" md="2" xl="1">
      <CFormLabel for="" class="col-form-label">발행일자</CFormLabel>
    </CCol>
    <CCol sm="8" md="4" xl="2">
      <DatePicker
        type="text"
        v-model="form.aa"
        placeholder="발행일자"
        maxlength="10"
        required
      />
    </CCol>
  </CRow>

  <CCollapse :visible="visible">
    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">발행회차</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <CFormInput
          type="text"
          placeholder="발행회차"
          maxlength="10"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">당회 납부기한</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <DatePicker
          type="text"
          v-model="form.aa"
          placeholder="당회 납부기한"
          maxlength="10"
          required
        />
      </CCol>
    </CRow>

    <CAlert color="secondary" class="text-right">
      <CButton color="success">업데이트</CButton>
    </CAlert>
  </CCollapse>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'

export default defineComponent({
  name: 'SalesBillIssueForm',
  components: { DatePicker },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      visible: false,
      form: {
        aa: '',
      },
    }
  },
  computed: {},
  methods: {},
})
</script>
