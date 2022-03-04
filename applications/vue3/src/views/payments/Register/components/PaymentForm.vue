<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <CRow class="mb-3">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label"> 수납일자</CFormLabel>
            <CCol sm="8">
              <DatePicker
                v-model="form.deal_date"
                required
                placeholder="거래일자"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">납부회차</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.installment_order" required>
                <option value="">---------</option>
                <option v-for="po in payOrderList" :value="po.pk" :key="po.pk">
                  {{ po.__str__ }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">수납금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.income"
                type="number"
                min="0"
                required
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">수납계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.bank_account" required>
                <option value="">---------</option>
                <option
                  v-for="pb in proBankAccountList"
                  :value="pb.pk"
                  :key="pb.pk"
                >
                  {{ pb.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol xs="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">입금자명</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.trader"
                v-c-tooltip="{
                  content:
                    '이 란은 반드시 해당 계좌에 기재된 입금자명과 일치하도록 기재하세요.',
                  placement: 'top',
                }"
                required
                placeholder="입금자명"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-2">
        <CCol>
          <CRow>
            <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
            <CCol sm="10">
              <CFormTextarea v-model="form.note" placeholder="기타 특이사항" />
            </CCol>
          </CRow>
        </CCol>
      </CRow>
    </CModalBody>

    <CModalFooter>
      <CButton type="button" color="light" @click="$emit('close')">
        닫기
      </CButton>
      <slot name="footer">
        <CButton
          :color="payment ? 'success' : 'primary'"
          :disabled="formsCheck"
        >
          저장
        </CButton>
        <CButton
          v-if="payment"
          type="button"
          color="danger"
          @click="$emit('on-delete')"
        >
          삭제
        </CButton>
      </slot>
    </CModalFooter>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'PayForm',
  components: { DatePicker },
  props: { contract: Object, payment: Object },
  data(this: any) {
    return {
      form: {
        project: '', // hidden -> index에서 처리
        sort: 1, // hidden -> always
        project_account_d1: '', // hidden
        project_account_d2: '', // hidden
        is_contract_payment: true, // hidden -> always
        contract: null, //  hidden -> 예외 및 신규 매칭 시 코드 확인
        content: '', // hidden

        installment_order: '',
        trader: '',
        bank_account: '',
        income: null,
        note: '',
        deal_date: new Date(),
      },
      validated: false,
    }
  },
  mounted(this: any) {
    if (this.payment) {
      this.form.installment_order = this.payment.installment_order.pk
      this.form.trader = this.payment.trader
      this.form.bank_account = this.payment.bank_account.pk
      this.form.income = this.payment.income
      this.form.note = this.payment.note
      this.form.deal_date = new Date(this.payment.deal_date)
    }
  },
  computed: {
    formsCheck() {
      if (this.payment) {
        const a =
          this.form.installment_order === this.payment.installment_order.pk
        const b = this.form.trader === this.payment.trader
        const c = this.form.bank_account === this.payment.bank_account.pk
        const d = this.form.income === this.payment.income
        const e = this.form.note === this.payment.note
        const f =
          this.form.deal_date.toString() ===
          new Date(this.payment.deal_date).toString()

        return a && b && c && d && e && f
      } else return false
    },
    ...mapState('payment', ['payOrderList']),
    ...mapState('proCash', ['proBankAccountList']),
  },
  watch: {
    contract(newVal) {
      this.form.project_account_d1 = newVal.order_group.sort
      this.form.project_account_d2 = newVal.order_group.sort
      this.form.contract = newVal.pk
      this.form.content = `${newVal.serial_number}[${newVal.constructor}] 대금납부`
    },
  },
  methods: {
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        this.form.deal_date = this.dateFormat(this.form.deal_date)
        const payload = this.payment
          ? { ...{ pk: this.payment.pk }, ...this.form }
          : this.form
        this.$emit('on-submit', payload)
      }
    },
  },
})
</script>
