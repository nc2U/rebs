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
      </CRow>

      <CRow class="mb-3">
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
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[대분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.account_d1"
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
      </CRow>

      <CRow class="mb-3">
        <CCol sm="6">
          <CRow>
            <CFormLabel class="col-sm-4 col-form-label">
              계정[중분류]
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.account_d2"
                @change="d2_change"
                required
                :disabled="form.account_d1 === ''"
              >
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
              <CFormSelect
                v-model="form.account_d3"
                required
                :disabled="form.account_d2 === ''"
              >
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
            <CFormLabel class="col-sm-4 col-form-label">
              {{ form.sort === '3' ? '출금' : '거래' }}계좌
            </CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account"
                required
                :disabled="form.sort === ''"
              >
                <option value="">---------</option>
                <option v-for="ba in comBankList" :value="ba.pk" :key="ba.pk">
                  {{ ba.alias_name }}
                </option>
              </CFormSelect>
            </CCol>
          </CRow>
        </CCol>
        <CCol sm="6">
          <CRow v-if="form.sort !== '3'">
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
          <CRow v-if="form.sort === '3'">
            <CFormLabel class="col-sm-4 col-form-label">입금계좌</CFormLabel>
            <CCol sm="8">
              <CFormSelect
                v-model="form.bank_account_to"
                required
                :disabled="form.sort !== '3'"
              >
                <option value="">---------</option>
                <option v-for="ba in comBankList" :value="ba.pk" :key="ba.pk">
                  {{ ba.alias_name }}
                </option>
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
        <CButton color="primary" :disabled="formsCheck">저장</CButton>
      </slot>
    </CModalFooter>
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import { mapActions, mapState } from 'vuex'

export default defineComponent({
  name: 'CashCreateForm',
  components: { DatePicker },
  data() {
    return {
      form: {
        // company: '',
        sort: '',
        account_d1: '',
        account_d2: '',
        account_d3: '',
        content: '',
        trader: '',
        bank_account: '',
        bank_account_to: '',
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
    this.callAccount()
  },
  computed: {
    ...mapState('comCash', [
      'formAccD1List',
      'formAccD2List',
      'formAccD3List',
      'comBankList',
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
      this.form.account_d1 = ''
      this.form.account_d2 = ''
      if (event.target.value === '1') this.form.outlay = null
      if (event.target.value === '2') this.form.income = null
      this.callAccount()
    },
    d1_change() {
      this.form.account_d2 = ''
      this.form.account_d3 = ''
      this.callAccount()
    },
    d2_change() {
      this.form.account_d3 = ''
      this.callAccount()
    },
    callAccount() {
      this.$nextTick(() => {
        const sort = this.form.sort
        const d1 = this.form.account_d1 ? this.form.account_d1 : null
        const d2 = this.form.account_d2 ? this.form.account_d2 : null
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
