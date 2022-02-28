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
              <CFormSelect v-model="form.sort" required @change="callAccount">
                <option v-show="form.sort === ''" value="">구분</option>
                <option v-show="form.sort === '1'" value="1">입금</option>
                <option v-show="form.sort === '2'" value="2">출금</option>
                <option v-show="form.sort === '3'" value="3">대체</option>
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
              <CFormSelect v-model="form.project_account_d2">
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
              <CFormInput v-model="form.content" placeholder="적요" />
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
                v-c-tooltip="{
                  content:
                    '분양대금(분담금) 항목일 경우 반드시 해당 계좌에 기재된 입금자를 기재.',
                  placement: 'top',
                }"
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
              <CFormSelect v-model="form.bank_account" required>
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
                min="0"
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
                min="0"
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
              <CFormTextarea v-model.number="form.note" placeholder="비고" />
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
  name: 'CreateForm',
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
    this.callAccount()
  },
  computed: {
    ...mapState('proCash', [
      'formAccD1List',
      'formAccD2List',
      'proBankAccountList',
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
        const d1 = this.form.project_account_d1
          ? this.form.project_account_d1
          : ''
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
