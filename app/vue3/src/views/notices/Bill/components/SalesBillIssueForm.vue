<template>
  <CAlert color="info">
    <CRow>
      <CCol xs="6" sm="7" md="8" lg="9" xl="10">
        <CIcon name="cil-arrow-circle-right" />
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
        v-model="published_date"
        v-maska="'####-##-##'"
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
          v-model="form.now_payment_order"
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
          v-model="form.now_due_date"
          v-maska="'####-##-##'"
          placeholder="당회 납부기한"
          maxlength="10"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">시행자명</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <CFormInput
          v-model="form.host_name"
          placeholder="시행자명"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">시행자 전화</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <input
          type="text"
          class="form-control"
          v-model="form.host_tel"
          v-maska="['###-###-####', '###-####-####']"
          placeholder="시행자 전화"
          maxlength="13"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">대행사명</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <CFormInput
          v-model="form.agency"
          placeholder="대행사명"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">대행사 전화</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="2">
        <input
          type="text"
          class="form-control"
          v-model="form.agency_tel"
          v-maska="['###-###-####', '###-####-####']"
          placeholder="대행사 전화"
          maxlength="13"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">수납은행[1]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_account1"
          placeholder="수납은행[1]"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">계좌번호[1]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_number1"
          placeholder="계좌번호[1]"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">예금주[1]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_host1"
          placeholder="예금주[1]"
          maxlength="20"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">수납은행[2]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_account2"
          placeholder="수납은행[2]"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">계좌번호[2]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_number2"
          placeholder="계좌번호[2]"
          maxlength="20"
          required
        />
      </CCol>

      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">예금주[2]</CFormLabel>
      </CCol>
      <CCol sm="8" md="4" xl="3">
        <CFormInput
          v-model="form.bank_host2"
          placeholder="예금주[2]"
          maxlength="20"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">시행자 주소</CFormLabel>
      </CCol>

      <CCol xs="4" sm="8" md="2" xl="1" class="mb-1">
        <CButton color="info">우편번호</CButton>
      </CCol>

      <CCol class="d-none d-sm-block d-md-none" sm="4" />

      <CCol xs="8" md="2" xl="1" class="mb-1">
        <input
          type="text"
          class="form-control"
          v-model="form.zipcode"
          v-maska="'#####'"
          placeholder="우편번호"
          maxlength="5"
          required
        />
      </CCol>

      <CCol class="d-none d-sm-block d-md-none" sm="4" />

      <CCol sm="8" md="6" xl="4" class="mb-1">
        <CFormInput
          v-model="form.address1"
          placeholder="메인 주소"
          maxlength="20"
          required
        />
      </CCol>

      <CCol class="d-none d-sm-block d-md-block d-xl-none" sm="4" md="2" />

      <CCol sm="8" md="5" xl="2" class="mb-1">
        <CFormInput
          v-model="form.address2"
          placeholder="상세 주소"
          maxlngth="20"
          required
        />
      </CCol>

      <CCol class="d-none d-sm-block d-md-none" sm="4" />

      <CCol sm="8" md="5" xl="3" class="mb-1">
        <CFormInput
          v-model="form.address3"
          placeholder="참고항목"
          maxlength="20"
          required
        />
      </CCol>
    </CRow>

    <CRow class="mb-1">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">고지서 제목</CFormLabel>
      </CCol>

      <CCol sm="8" md="10" lg="12" xl="11">
        <CFormInput
          v-model="form.title"
          placeholder="고재서 제목"
          maxlength="20"
          required
        />
      </CCol>
      <CCol class="d-none d-md-block d-lg-none" md="6" />
    </CRow>

    <CRow class="mb-3">
      <CCol sm="4" md="2" xl="1">
        <CFormLabel for="" class="col-form-label">고지서 내용</CFormLabel>
      </CCol>
      <CCol sm="8" md="10" lg="12" xl="11">
        <CFormTextarea
          v-model="form.content"
          placeholder="고지서 내용"
          rows="4"
        />
      </CCol>
      <CCol class="d-none d-md-block d-lg-none" md="6" />
    </CRow>

    <CAlert color="secondary" class="text-right">
      <CButton color="success">업데이트</CButton>
    </CAlert>
  </CCollapse>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import { maska } from 'maska'

export default defineComponent({
  name: 'SalesBillIssueForm',
  directives: { maska },
  components: { DatePicker },
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      visible: false,
      published_date: new Date(),
      form: {
        now_payment_order: '',
        now_due_date: '',
        host_name: '',
        host_tel: '',
        agency: '',
        agency_tel: '',
        bank_account1: '',
        bank_number1: '',
        bank_host1: '',
        bank_account2: '',
        bank_number2: '',
        bank_host2: '',
        zipcode: '',
        address1: '',
        address2: '',
        address3: '',
        title: '',
        content: '',
      },
    }
  },
  computed: {},
  methods: {},
})
</script>
