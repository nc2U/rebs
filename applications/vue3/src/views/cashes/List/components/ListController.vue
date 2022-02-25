<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="8">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <CFormInput
              v-model="form.from_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormInput
              v-model="form.to_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.sort1" @change="accountD1Select">
              <option value="">구분</option>
              <option value="1">입금</option>
              <option value="2">출금</option>
              <option value="3">대체</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.sort1" @change="accountD1Select">
              <option value="">구분</option>
              <option value="1">입금</option>
              <option value="2">출금</option>
              <option value="3">대체</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.sort2" @change="accountD2Select">
              <option value="">분류</option>
              <option v-for="acc in comAccD1List" :value="acc.pk" :key="acc.pk">
                {{ acc.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.account" @change="listFiltering(1)">
              <option value="">계정과목</option>
              <option v-for="acc in comAccD3List" :value="acc.pk" :key="acc.pk">
                {{ acc.name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="4">
        <CRow>
          <CCol md="6" lg="4" class="mb-3">
            <CFormSelect v-model="form.bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option v-for="acc in comBankList" :value="acc.pk" :key="acc.pk">
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="8" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                @keydown.enter="listFiltering(1)"
                placeholder="적요, 거래처 검색"
                aria-label="Username"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="listFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <CRow>
      <CCol color="warning" class="p-2 pl-3">
        <strong>
          거래 건수 조회 결과 : {{ numFormat(cashBookCount) }} 건
        </strong>
      </CCol>
      <CCol class="text-right mb-0" v-if="!formsCheck">
        <CButton color="info" @click="resetForm" size="sm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  directives: { maska },
  data() {
    return {
      form: {
        from_date: '',
        to_date: '',
        sort1: '',
        sort2: '',
        account: '',
        bank_account: '',
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.from_date === ''
      const b = this.form.to_date === ''
      const c = this.form.sort1 === ''
      const d = this.form.sort2 === ''
      const e = this.form.account === ''
      const f = this.form.bank_account === ''
      const g = this.form.search === ''
      return a && b && c && d && e && f && g
    },
    ...mapState('comCash', [
      'comAccD1List',
      'comAccD2List',
      'comAccD3List',
      'comBankList',
      'cashBookCount',
    ]),
  },
  methods: {
    accountD1Select() {
      this.listFiltering(1)
      this.form.sort2 = ''
      this.form.account = ''
      // this.$nextTick(() => this.$emit('d1-select', this.form.accountD1))
    },
    accountD2Select() {
      this.listFiltering(1)
      this.form.account = ''
      this.$nextTick(() => this.$emit('d1-select', this.form.account))
    },
    listFiltering(page = 1) {
      this.$nextTick(() =>
        this.$emit('payment-filtering', { ...{ page }, ...this.form }),
      )
    },
    resetForm() {
      this.form.from_date = ''
      this.form.to_date = ''
      this.form.sort1 = ''
      this.form.sort2 = ''
      this.form.account = ''
      this.form.bank_account = ''
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
