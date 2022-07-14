<template>
  <CAlert color="info">
    <CRow>
      <CCol xs="6" sm="7" md="8" lg="9" xl="10">
        <CIcon name="cibAddthis" />
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

  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
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
          <CFormSelect
            v-model="form.now_payment_order"
            placeholder="발행회차"
            maxlength="10"
            required
          >
            <option value="">--------</option>
            <option v-for="po in payOrderList" :value="po.pk" :key="po.pk">
              {{ po.__str__ }}
            </option>
          </CFormSelect>
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
            :required="false"
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
          />
        </CCol>
      </CRow>

      <CRow class="mb-1">
        <CCol sm="4" md="2" xl="1">
          <CFormLabel for="" class="col-form-label">시행자 주소</CFormLabel>
        </CCol>

        <CCol xs="12" sm="8" md="4" xl="2" class="mb-1">
          <CInputGroup>
            <CInputGroupText @click="$refs.postCode.initiate()">
              우편번호
            </CInputGroupText>
            <CFormInput
              type="text"
              v-model="form.zipcode"
              v-maska="'#####'"
              placeholder="우편번호"
              maxlength="5"
              required
              @focus="$refs.postCode.initiate()"
            />
            <!--            <CFormFeedback invalid>우편번호를 입력하세요.</CFormFeedback>-->
          </CInputGroup>
        </CCol>

        <CCol class="d-none d-sm-block d-md-none" sm="4" />

        <CCol sm="8" md="6" xl="4" class="mb-1">
          <CFormInput
            v-model="form.address1"
            @click="$refs.postCode.initiate()"
            placeholder="메인 주소"
            maxlength="20"
            required
          />
        </CCol>

        <CCol class="d-none d-sm-block d-md-block d-xl-none" sm="4" md="2" />

        <CCol sm="8" md="5" xl="2" class="mb-1">
          <CFormInput
            v-model="form.address2"
            ref="address2"
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
        <CButton type="submit" :color="btnClass" :disabled="formsCheck">
          {{ confirmText }}
        </CButton>
      </CAlert>
    </CCollapse>
  </CForm>

  <DaumPostcode @addressPut="addressPut" ref="postCode" />

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cilChevronCircleRightAlt" />
      수납 고지서 발행 정보
    </template>
    <template v-slot:default>
      수납 고지서 발행 정보 {{ confirmText }}을(를) 진행하시겠습니까?
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
import { maska } from 'maska'
import { mapGetters, mapState } from 'vuex'

export default defineComponent({
  name: 'SalesBillIssueForm',
  components: { DatePicker, ConfirmModal, AlertModal, DaumPostcode },
  mixins: [addressMixin],
  directives: { maska },
  props: {
    bill_issue: Object,
  },
  data() {
    return {
      visible: false,
      published_date: new Date(),
      now_order: null,
      pk: '',
      form: {
        now_payment_order: '',
        now_due_date: null,
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
      validated: false,
    }
  },
  mounted() {
    if (this.bill_issue) {
      this.pk = this.bill_issue.pk
      this.form.now_payment_order = this.bill_issue.now_payment_order
      this.form.host_name = this.bill_issue.host_name
      this.form.host_tel = this.bill_issue.host_tel
      this.form.agency = this.bill_issue.agency
      this.form.agency_tel = this.bill_issue.agency_tel
      this.form.bank_account1 = this.bill_issue.bank_account1
      this.form.bank_number1 = this.bill_issue.bank_number1
      this.form.bank_host1 = this.bill_issue.bank_host1
      this.form.bank_account2 = this.bill_issue.bank_account2
      this.form.bank_number2 = this.bill_issue.bank_number2
      this.form.bank_host2 = this.bill_issue.bank_host2
      this.form.zipcode = this.bill_issue.zipcode
      this.form.address1 = this.bill_issue.address1
      this.form.address2 = this.bill_issue.address2
      this.form.address3 = this.bill_issue.address3
      this.form.title = this.bill_issue.title
      this.form.content = this.bill_issue.content
    }
  },
  computed: {
    confirmText() {
      return this.bill_issue ? '업데이트' : '신규등록'
    },
    btnClass() {
      return this.bill_issue ? 'success' : 'primary'
    },
    formsCheck(this: any) {
      if (this.bill_issue) {
        const a =
          this.form.now_payment_order === this.bill_issue.now_payment_order
        const b = this.form.now_due_date === this.now_order.pay_due_date
        const c = this.form.host_name === this.bill_issue.host_name
        const d = this.form.host_tel === this.bill_issue.host_tel
        const e = this.form.agency === this.bill_issue.agency
        const f = this.form.agency_tel === this.bill_issue.agency_tel
        const g = this.form.bank_account1 === this.bill_issue.bank_account1
        const h = this.form.bank_number1 === this.bill_issue.bank_number1
        const i = this.form.bank_host1 === this.bill_issue.bank_host1
        const j = this.form.bank_account2 === this.bill_issue.bank_account2
        const k = this.form.bank_number2 === this.bill_issue.bank_number2
        const l = this.form.bank_host2 === this.bill_issue.bank_host2
        const m = this.form.zipcode === this.bill_issue.zipcode
        const n = this.form.address1 === this.bill_issue.address1
        const o = this.form.address2 === this.bill_issue.address2
        const p = this.form.address3 === this.bill_issue.address3
        const q = this.form.title === this.bill_issue.title
        const r = this.form.content === this.bill_issue.content
        const sky = a && b && c && d && e && f && g && h && i
        const land = j && k && l && m && n && o && p && q && r
        return sky && land
      }
      return false
    },
    writeAuth() {
      return this.superAuth || (this.staffAuth && this.staffAuth.notice === '2')
    },
    ...mapState('payment', ['payOrderList']),
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  watch: {
    bill_issue(val) {
      if (val) {
        this.get_now_order(val.now_payment_order)

        this.pk = val.pk
        this.form.now_payment_order = val.now_payment_order
        this.form.host_name = val.host_name
        this.form.host_tel = val.host_tel
        this.form.agency = val.agency
        this.form.agency_tel = val.agency_tel
        this.form.bank_account1 = val.bank_account1
        this.form.bank_number1 = val.bank_number1
        this.form.bank_host1 = val.bank_host1
        this.form.bank_account2 = val.bank_account2
        this.form.bank_number2 = val.bank_number2
        this.form.bank_host2 = val.bank_host2
        this.form.zipcode = val.zipcode
        this.form.address1 = val.address1
        this.form.address2 = val.address2
        this.form.address3 = val.address3
        this.form.title = val.title
        this.form.content = val.content
      }
    },
    now_order(val) {
      if (val) {
        this.form.now_due_date = val.pay_due_date
      }
    },
    published_date(this: any, val) {
      this.$emit('set-pub-date', this.dateFormat(val))
    },
  },
  methods: {
    get_now_order(np_order: number) {
      this.now_order = this.payOrderList
        .filter((o: any) => o.pk == np_order)
        .map((o: any) => o)[0]
      this.$emit('get-now-order', this.now_order)
    },
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
      this.form.now_due_date = this.form.now_due_date
        ? this.dateFormat(this.form.now_due_date)
        : null
      let payload
      if (this.bill_issue) {
        payload = { ...{ pk }, ...this.form }
      } else {
        payload = this.form
      }
      this.$emit('on-submit', payload)

      this.validated = false
      this.$refs.confirmModal.visible = false
    },
  },
})
</script>
