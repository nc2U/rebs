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
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.sort" @change="callAccount">
                <option v-show="form.sort === ''" value="">구분</option>
                <option v-show="form.sort === '1'" value="1">입금</option>
                <option v-show="form.sort === '2'" value="2">출금</option>
                <option v-show="form.sort === '3'" value="3">대체</option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[대분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.account_d1" @change="callAccount">
                <option value="">---------</option>
                <option v-for="d1 in formAccD1List" :value="d1.pk" :key="d1.pk">
                  {{ d1.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[중분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.account_d2" @change="callAccount">
                <option value="">---------</option>
                <option v-for="d2 in formAccD2List" :value="d2.pk" :key="d2.pk">
                  {{ d2.name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[소분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.account_d3">
                <option value="">---------</option>
                <option v-for="d3 in formAccD3List" :value="d3.pk" :key="d3.pk">
                  {{ d3.name }}
                </option>
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
        <CButton color="success" :disabled="formsCheck">저장</CButton>
      </slot>
    </CModalFooter>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'CashForm',
  props: {
    cash: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        company: '',
        sort: '',
        account_d1: '',
        account_d2: '',
        account_d3: '',
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
    if (this.cash) {
      this.form.company = this.cash.company
      this.form.sort = this.cash.sort
      this.form.account_d1 = this.cash.account_d1
      this.form.account_d2 = this.cash.account_d2
      this.form.account_d3 = this.cash.account_d3
      this.form.content = this.cash.content
      this.form.trader = this.cash.trader
      this.form.bank_account = this.cash.bank_account
      this.form.income = this.cash.income
      this.form.outlay = this.cash.outlay
      this.form.evidence = this.cash.evidence
      this.form.note = this.cash.note
      this.form.deal_date = this.cash.deal_date
    }
    this.callAccount()
  },
  computed: {
    formsCheck() {
      const a = this.form.company === this.cash.company
      const b = this.form.sort === this.cash.sort
      const c = this.form.account_d1 === this.cash.account_d1
      const d = this.form.account_d2 === this.cash.account_d2
      const e = this.form.account_d3 === this.cash.account_d3
      const f = this.form.content === this.cash.content
      const g = this.form.trader === this.cash.trader
      const h = this.form.bank_account === this.cash.bank_account
      const i = this.form.income === this.cash.income
      const j = this.form.outlay === this.cash.outlay
      const k = this.form.evidence === this.cash.evidence
      const l = this.form.note === this.cash.note
      const m = this.form.deal_date === this.cash.deal_date

      return a && b && c && d && e && f && g && h && i && j && k && l && m
    },
    ...mapState('comCash', [
      'sortList',
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
      this.$nextTick(() => {
        const sort = this.form.sort
        const d1 = this.form.account_d1 ? this.form.account_d1 : ''
        const d2 = this.form.account_d2 ? this.form.account_d2 : ''
        this.fetchFormAccD1List({ sort })
        this.fetchFormAccD2List({ sort, d1 })
        this.fetchFormAccD3List({ sort, d1, d2 })
      })
    },
    ...mapActions('comCash', [
      'fetchFormAccD1List',
      'fetchFormAccD2List',
      'fetchFormAccD3List',
    ]),
  },
})
</script>
