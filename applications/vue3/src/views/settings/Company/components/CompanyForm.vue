<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CCardBody>
      <CRow class="mb-3">
        <CFormLabel for="companyName" class="col-md-2 col-form-label">
          회사명
        </CFormLabel>

        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.name"
            placeholder="회사명을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>회사명을 입력하세요.</CFormFeedback>
        </CCol>

        <CFormLabel for="companyCeo" class="col-md-2 col-form-label">
          대표자명
        </CFormLabel>

        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.ceo"
            placeholder="대표자명을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>대표자명을 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="taxNumber" class="col-md-2 col-form-label">
          사업자등록번호
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.tax_number"
            placeholder="사업자번호를 입력하세요"
            v-maska="'###-##-#####'"
            maxlength="12"
            required
          />
          <CFormFeedback invalid>사업자등록번호를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="orgNumber" class="col-md-2 col-form-label">
          법인등록번호
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.org_number"
            placeholder="법인등록번호를 입력하세요"
            v-maska="'######-#######'"
            maxlength="14"
            required
          />
          <CFormFeedback invalid>법인등록번호를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="businessCond" class="col-md-2 col-form-label">
          업태
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.business_cond"
            placeholder="업태를 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>업태를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="businessEven" class="col-md-2 col-form-label">
          종목
        </CFormLabel>
        <CCol md="4">
          <CFormInput
            type="text"
            v-model="form.business_even"
            placeholder="종목을 입력하세요"
            maxlength="20"
            required
          />
          <CFormFeedback invalid>종목을 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CFormLabel for="esDate" class="col-md-2 col-form-label">
          설립일자
        </CFormLabel>
        <CCol md="4">
          <DatePicker
            type="text"
            v-model="form.es_date"
            maxlength="10"
            placeholder="설립일자를 입력하세요"
            v-maska="'####-##-##'"
            required
          />
          <CFormFeedback invalid>설립일자를 입력하세요.</CFormFeedback>
        </CCol>
        <CFormLabel for="opDate" class="col-md-2 col-form-label">
          개업일자
        </CFormLabel>
        <CCol md="4">
          <DatePicker
            type="text"
            v-model="form.op_date"
            maxlength="10"
            placeholder="개업일자를 입력하세요"
            v-maska="'####-##-##'"
            required
          />
          <CFormFeedback invalid>개업일자를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>

      <hr />

      <CRow>
        <CFormLabel for="zipcode" class="col-md-2 col-form-label">
          회사주소
        </CFormLabel>
        <CCol md="4" xl="2" class="mb-3">
          <CInputGroup>
            <CFormInput
              type="text"
              v-model="form.zipcode"
              placeholder="우편번호"
              maxlength="5"
              required
              @focus="$refs.postCode.initiate()"
            />
            <CInputGroupText @click="$refs.postCode.initiate()">
              우편번호
            </CInputGroupText>
            <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>
          </CInputGroup>
        </CCol>
      </CRow>
      <CRow>
        <CCol sm="2"></CCol>
        <CCol md="10" lg="4" class="mb-3">
          <CFormInput
            type="text"
            v-model="form.address1"
            placeholder="회사주소를 입력하세요"
            maxlength="50"
            required
            @focus="$refs.postCode.initiate()"
          />
          <CFormFeedback invalid>회사주소를 입력하세요.</CFormFeedback>
        </CCol>
        <CCol xs="2" class="d-none d-md-block d-lg-none"></CCol>
        <CCol md="5" lg="3" class="mb-3">
          <CFormInput
            type="text"
            v-model="form.address2"
            ref="address2"
            placeholder="상세주소를 입력하세요"
            maxlength="30"
            required
          />
          <CFormFeedback invalid>상세주소를 입력하세요.</CFormFeedback>
        </CCol>
        <CCol md="5" lg="3" class="mb-3">
          <CFormInput
            type="text"
            v-model="form.address3"
            placeholder="나머지 주소를 입력하세요"
            maxlength="30"
          />
          <CFormFeedback invalid>나머지 주소를 입력하세요.</CFormFeedback>
        </CCol>
      </CRow>
    </CCardBody>

    <CCardFooter class="text-right">
      <CButton type="button" color="light" @click="this.$emit('reset-form')">
        취소
      </CButton>
      <CButton
        type="button"
        v-if="update"
        color="danger"
        @click="deleteCompany"
      >
        삭제
      </CButton>
      <CButton type="submit" :color="btnClass" :disabled="formsCheck">
        <CIcon name="cil-check-circle" />
        저장
      </CButton>
    </CCardFooter>
  </CForm>

  <DaumPostcode @addressPut="addressPut" ref="postCode" />

  <ConfirmModal ref="delModal">
    <template v-slot:header>회사정보</template>
    <template v-slot:default>현재 삭제 기능이 구현되지 않았습니다.</template>
    <template v-slot:footer>
      <CButton color="danger" disabled="">삭제</CButton>
    </template>
  </ConfirmModal>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>회사정보</template>
    <template v-slot:default>
      회사정보 {{ confirmText }}을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton :color="btnClass" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import DaumPostcode from '@/components/DaumPostcode/index.vue'
import addressMixin from '@/components/DaumPostcode/addressMixin'
import { mapGetters } from 'vuex'
import { maska } from 'maska'

export default defineComponent({
  name: 'CompanyForm',
  components: { DatePicker, DaumPostcode, ConfirmModal, AlertModal },
  mixins: [addressMixin],
  directives: { maska },
  data() {
    return {
      pk: '',
      form: {
        name: '',
        ceo: '',
        tax_number: '',
        org_number: '',
        business_cond: '',
        business_even: '',
        es_date: new Date(),
        op_date: new Date(),
        zipcode: '',
        address1: '',
        address2: '',
        address3: '',
      },
      validated: false,
    }
  },
  created() {
    if (this.update && this.company) {
      this.pk = this.company.pk
      this.form.name = this.company.name
      this.form.ceo = this.company.ceo
      this.form.tax_number = this.company.tax_number
      this.form.org_number = this.company.org_number
      this.form.business_cond = this.company.business_cond
      this.form.business_even = this.company.business_even
      this.form.es_date = new Date(this.company.es_date)
      this.form.op_date = new Date(this.company.op_date)
      this.form.zipcode = this.company.zipcode
      this.form.address1 = this.company.address1
      this.form.address2 = this.company.address2
      this.form.address3 = this.company.address3
    }
  },
  props: {
    company: Object,
    update: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    confirmText() {
      return this.update ? '변경' : '등록'
    },
    btnClass() {
      return this.update ? 'success' : 'primary'
    },
    formsCheck(this: any) {
      const a = this.form.name === this.company.name
      const b = this.form.ceo === this.company.ceo
      const c = this.form.tax_number === this.company.tax_number
      const d = this.form.org_number === this.company.org_number
      const e = this.form.business_cond === this.company.business_cond
      const f = this.form.business_even === this.company.business_even
      const g =
        new Date(this.form.es_date).toString() ===
        new Date(this.company.es_date).toString()
      const h =
        new Date(this.form.op_date).toString() ===
        new Date(this.company.op_date).toString()
      const i = this.form.zipcode === this.company.zipcode
      const j = this.form.address1 === this.company.address1
      const k = this.form.address2 === this.company.address2
      const l = this.form.address3 === this.company.address3

      return a && b && c && d && e && f && g && h && i && j && k && l
    },
    writeAuth() {
      const create = this.superAuth ? true : false
      const update =
        this.superAuth ||
        (this.staffAuth && this.staffAuth.company_settings === '2')
      return this.update ? update : create
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    onSubmit(this: any, event: any) {
      if (this.writeAuth) {
        const form = event.currentTarget
        if (form.checkValidity() === false) {
          event.preventDefault()
          event.stopPropagation()

          this.validated = true
        } else {
          this.$refs.confirmModal.callModal()
        }
      } else {
        this.$refs.alertModal.callModal()
      }
    },
    modalAction(this: any) {
      const { pk } = this
      this.form.es_date = this.dateFormat(this.form.es_date)
      this.form.op_date = this.dateFormat(this.form.op_date)
      if (this.update) {
        this.$emit('to-update', { ...{ pk }, ...this.form })
      } else {
        this.$emit('to-create', this.form)
      }
      this.validated = false
    },
    deleteCompany(this: any) {
      if (this.superAuth) this.$refs.delModal.callModal()
      else this.$refs.alertModal.callModal()
    },
  },
})
</script>
