<template>
  <CForm>
    <CRow class="mb-3">
      <CCol sm="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">거래일자</CFormLabel>
          <CCol sm="8">
            <CFormInput v-model="form.deal_date" placeholder="거래일자" />
          </CCol>
        </CRow>
      </CCol>
      <CCol sm="6">
        <CRow></CRow>
      </CCol>
    </CRow>

    <CRow class="mb-3">
      <CCol sm="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">구분</CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="form.sort">
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
          <CFormLabel class="col-sm-4 col-form-label">계정[대분류]</CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="form.account_d1">
              <option value="">---------</option>
              <option v-for="d1 in comAccD1List" :value="d1.pk" :key="d1.pk">
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
          <CFormLabel class="col-sm-4 col-form-label">계정[중분류]</CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="form.account_d2">
              <option value="">---------</option>
              <option v-for="d2 in comAccD2List" :value="d2.pk" :key="d2.pk">
                {{ d2.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol sm="6">
        <CRow>
          <CFormLabel class="col-sm-4 col-form-label">계정[소분류]</CFormLabel>
          <CCol sm="8">
            <CFormSelect v-model="form.account_d3">
              <option value="">---------</option>
              <option v-for="d3 in comAccD3List" :value="d3.pk" :key="d3.pk">
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
            <CFormInput v-model="form.bank_account" placeholder="거래계좌" />
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
  </CForm>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'CashForm',
  props: {
    form: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {}
  },
  data() {
    return {
      sample: '',
    }
  },
  computed: {
    ...mapState('comCash', [
      'comAccD1List',
      'comAccD2List',
      'comAccD3List',
      'comBankList',
      'cashBookCount',
    ]),
  },
  methods: {},
})
</script>
