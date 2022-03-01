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
              <DatePicker v-model="form.date" required placeholder="거래일자" />
            </CCol>
          </CRow>
        </CCol>

        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
            <CCol sm="8">
              <CFormSelect v-model="form.sort" required @change="sort_change">
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
                @change="d1_change"
                required
                :disabled="form.sort === ''"
              >
                <option value="">---------</option>
                <option v-for="d1 in formAccD1List" :value="d1.pk" :key="d1.pk">
                  {{ d1.name }}
                </option>
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
              <CFormSelect
                v-model="form.project_account_d2"
                required
                :disabled="form.project_account_d1 === ''"
              >
                <option value="">---------</option>
                <option v-for="d2 in formAccD2List" :value="d2.pk" :key="d2.pk">
                  {{ d2.name }}
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
              <CFormInput
                v-model="form.content"
                placeholder="적요"
                required
                :disabled="form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래처</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model="form.trader"
                v-c-tooltip="{
                  content:
                    '분양대금(분담금) 항목일 경우 반드시 해당 계좌에 기재된 입금자를 기재.',
                  placement: 'top',
                }"
                placeholder="거래처"
                required
                :disabled="form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">거래계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account"
                required
                :disabled="form.sort === ''"
              >
                <option value="">---------</option>
                <option
                  v-for="ba in proBankAccountList"
                  :value="ba.pk"
                  :key="ba.pk"
                >
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
              <CFormSelect v-model="form.evidence" :disabled="form.sort === ''">
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
            <CFormLabel class="col-sm-4 col-form-label">출금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.outlay"
                type="number"
                min="0"
                placeholder="출금액"
                :required="form.sort === '2'"
                :disabled="form.sort === '1' || form.sort === ''"
              />
            </CCol>
          </CRow>
        </CCol>

        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">입금액</CFormLabel>
            <CCol sm="8">
              <CFormInput
                v-model.number="form.income"
                type="number"
                min="0"
                placeholder="입금액"
                :required="form.sort === '1'"
                :disabled="form.sort === '2' || form.sort === ''"
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
                placeholder="비고"
                :disabled="form.sort === ''"
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
import DatePicker from '@/components/DatePicker/index.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'UpdateForm',
  components: { DatePicker },
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
        content: '',
        trader: '',
        bank_account: '',
        income: null,
        outlay: null,
        evidence: '0',
        note: '',
        date: new Date(),
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
      this.form.content = this.proCash.content
      this.form.trader = this.proCash.trader
      this.form.bank_account = this.proCash.bank_account
      this.form.income = this.proCash.income
      this.form.outlay = this.proCash.outlay
      this.form.evidence = this.proCash.evidence
      this.form.note = this.proCash.note
      this.form.date = new Date(this.proCash.deal_date)
    }
    this.callAccount()
  },
  computed: {
    formsCheck() {
      const a = this.form.project === this.proCash.project
      const b = this.form.sort === this.proCash.sort
      const c = this.form.project_account_d1 === this.proCash.project_account_d1
      const d = this.form.project_account_d2 === this.proCash.project_account_d2
      const e = this.form.content === this.proCash.content
      const f = this.form.trader === this.proCash.trader
      const g = this.form.bank_account === this.proCash.bank_account
      const h = this.form.income === this.proCash.income
      const i = this.form.outlay === this.proCash.outlay
      const j = this.form.evidence === this.proCash.evidence
      const k = this.form.note === this.proCash.note
      const l =
        this.form.date.toString() ===
        new Date(this.proCash.deal_date).toString()

      return a && b && c && d && e && f && g && h && i && j && k && l
    },
    ...mapState('proCash', [
      'formAccD1List',
      'formAccD2List',
      'proBankAccountList',
    ]),
  },
  methods: {
    onSubmit(this: any, event: any) {
      const form = event.currentTarget
      if (form.checkValidity() === false) {
        event.preventDefault()
        event.stopPropagation()

        this.validated = true
      } else {
        const { date, ...formData } = this.form
        const deal_date = this.dateFormat(date)
        this.$emit('on-submit', { ...{ deal_date }, ...formData })
      }
    },
    sort_change(event: any) {
      if (event.target.value === '1') this.form.outlay = null
      if (event.target.value === '2') this.form.income = null
      if (event.target.value === '3') {
        this.form.project_account_d1 = '17'
        this.form.project_account_d2 = '61'
      } else {
        this.form.project_account_d1 = ''
        this.form.project_account_d2 = ''
      }
      this.callAccount()
    },
    d1_change() {
      this.form.project_account_d2 = ''
      this.callAccount()
    },
    callAccount() {
      this.$nextTick(() => {
        const sort = this.form.sort
        const d1 = this.form.project_account_d1
        this.fetchProFormAccD1List(sort)
        this.fetchProFormAccD2List({ sort, d1 })
      })
    },
    ...mapActions('proCash', [
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
    ]),
  },
})
</script>
