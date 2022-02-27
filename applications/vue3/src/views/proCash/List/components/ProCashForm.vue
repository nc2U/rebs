<template>
  <CForm
    class="needs-validation"
    novalidate
    :validated="validated"
    @submit.prevent="onSubmit"
  >
    <CModalBody class="p-4">
      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래일자</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.deal_date"
                required
                placeholder="거래일자"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.sort" @change="callAccount">
                <option value="">구분</option>
                <option value="1">입금</option>
                <option value="2">출금</option>
                <option value="3">대체</option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[상위분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.project_account_d1"
                @change="callAccount"
              >
                <option value="">---------</option>
                <!--                <option v-for="d2 in formAccD2List" :value="d2.pk" :key="d2.pk">-->
                <!--                  {{ d2.name }}-->
                <!--                </option>-->
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[하위분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.project_account_d2">
                <option value="">---------</option>
                <!--                <option v-for="d3 in formAccD3List" :value="d3.pk" :key="d3.pk">-->
                <!--                  {{ d3.name }}-->
                <!--                </option>-->
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">적요</CFormLabel>
            <CCol sm="8">
              <CFormInput v-model="form.content" placeholder="적요" />
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래처</CFormLabel>
            <CCol sm="8">
              <CFormInput v-model="form.trader" placeholder="거래처" />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.bank_account">
                <option value="">---------</option>
                <option v-for="ba in comBankList" :value="ba.pk" :key="ba.pk">
                  {{ ba.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">증빙자료</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.evidence">
                <option value="0">---------</option>
                <option value="1">세금계산서</option>
                <option value="2">계산서(면세)</option>
                <option value="3">신용카드전표</option>
                <option value="4">현금영수증</option>
                <option value="5">간이영수증</option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">입금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.income"
                type="number"
                placeholder="입금액"
                :disabled="form.sort === '2'"
              />
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">출금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.outlay"
                type="number"
                placeholder="출금액"
                :disabled="form.sort === '1'"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="12">
          <CRow>
            <CFormLabel class="col-sm-2 col-form-label">비고</CFormLabel>
            <CCol sm="10">
              <CFormTextarea
                v-model.number="form.note"
                type="number"
                placeholder="비고"
              />
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
        <CButton color="success">저장</CButton>
      </slot>
    </CModalFooter>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'ProCashForm',
  props: {
    proCash: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        project: '',
        sort: '',
        project_account_d1: '',
        project_account_d2: '',
        // is_record_separate: '',
        is_contract_payment: '',
        // contract: '',
        // installment_order: '',
        // is_release: '',
        // is_refund_contractor: '',
        content: '',
        trader: '',
        bank_account: '',
        income: '',
        outlay: '',
        evidence: '',
        note: '',
        deal_date: '',
      },
      validated: false,
    }
  },
  created() {
    if (this.proCash) {
      this.form.project = this.proCash.project
      this.form.sort = this.proCash.sort
      this.form.project_account_d1 = this.proCash.project_account_d1
      this.form.project_account_d2 = this.proCash.project_account_d2
      // this.form.is_record_separate = this.proCash.is_record_separate
      this.form.is_contract_payment = this.proCash.is_contract_payment
      // this.form.contract = this.proCash.contract
      // this.form.installment_order = this.proCash.installment_order
      // this.form.is_release = this.proCash.is_release
      // this.form.is_refund_contractor = this.proCash.is_refund_contractor
      this.form.content = this.proCash.content
      this.form.trader = this.proCash.trader
      this.form.bank_account = this.proCash.bank_account
      this.form.income = this.proCash.income
      this.form.outlay = this.proCash.outlay
      this.form.evidence = this.proCash.evidence
      this.form.note = this.proCash.note
      this.form.deal_date = this.proCash.deal_date
    }
    this.callAccount()
  },
  computed: {
    formsCheck() {
      // const a = this.form.dr
      return true
    },
    ...mapState('comCash', [
      'formAccD1List',
      'formAccD2List',
      'formAccD3List',
      'comBankList',
    ]),
  },
  methods: {
    onSubmit(event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        this.$emit('on-submit', this.form)
      }
    },
    callAccount() {
      // this.$nextTick(() => {
      //   const sort = this.form.sort
      //
      //   const is_d1 = this.form.account_d1
      //     ? this.formAccD1List.filter(
      //         (d1: any) => d1.pk === this.form.account_d1,
      //       ).length
      //     : 0
      //   const is_d2 = this.form.account_d2
      //     ? this.formAccD2List.filter(
      //         (d2: any) => d2.pk === this.form.account_d2,
      //       ).length
      //     : 0
      //   const d1 = this.form.account_d1 && is_d1 ? this.form.account_d1 : ''
      //   const d2 = this.form.account_d2 && is_d2 ? this.form.account_d2 : ''
      //
      //   this.fetchAccountD1List({ sort })
      //   this.fetchAccountD2List({ sort, d1 })
      //   this.fetchAccountD3List({ sort, d1, d2 })
      // })
    },
    ...mapActions('comCash', [
      'fetchAccountD1List',
      'fetchAccountD2List',
      'fetchAccountD3List',
    ]),
  },
})
</script>
