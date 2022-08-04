<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="3">
        <CRow>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.sort" @change="sortSelect">
              <option value="">구분</option>
              <option value="1">입금</option>
              <option value="2">출금</option>
              <option value="3">대체</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.account_d1" @change="accountD1Select">
              <option value="">계정[대분류]</option>
              <option
                v-for="acc1 in formAccD1List"
                :key="acc1.pk"
                :value="acc1.pk"
              >
                {{ acc1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="form.account_d2"
              :disabled="!form.account_d1"
              @change="accountD2Select"
            >
              <option value="">계정[중분류]</option>
              <option
                v-for="acc2 in formAccD2List"
                :key="acc2.pk"
                :value="acc2.pk"
              >
                {{ acc2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="form.account_d3"
              :disabled="!form.account_d1"
              @change="listFiltering(1)"
            >
              <option value="">계정[소분류]</option>
              <option
                v-for="acc3 in formAccD3List"
                :key="acc3.pk"
                :value="acc3.pk"
              >
                {{ acc3.name }}
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
              <option v-for="acc in comBankList" :key="acc.pk" :value="acc.pk">
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="8" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="적요, 거래처 검색"
                aria-label="Username"
                aria-describedby="addon-wrapping"
                @keydown.enter="listFiltering(1)"
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
      <CCol v-if="!formsCheck" class="text-right mb-0">
        <CButton color="info" size="sm" @click="resetForm">
          검색조건 초기화
        </CButton>
      </CCol>
    </CRow>
  </CCallout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import DatePicker from '@/components/DatePicker/index.vue'
import { maska } from 'maska'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  components: { DatePicker },
  directives: { maska },
  data() {
    return {
      from_date: '',
      to_date: '',
      form: {
        sort: '',
        account_d1: '',
        account_d2: '',
        account_d3: '',
        bank_account: '',
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.from_date === ''
      const b = this.to_date === ''
      const c = this.form.sort === ''
      const d = this.form.account_d1 === ''
      const e = this.form.account_d2 === ''
      const f = this.form.account_d3 === ''
      const g = this.form.bank_account === ''
      const h = this.form.search === ''
      return a && b && c && d && e && f && g && h
    },
    ...mapState('comCash', [
      'formAccD1List',
      'formAccD2List',
      'formAccD3List',
      'comBankList',
      'cashBookCount',
    ]),
  },
  watch: {
    from_date() {
      this.listFiltering(1)
    },
    to_date() {
      this.listFiltering(1)
    },
  },
  methods: {
    sortSelect() {
      this.listFiltering(1)
      this.form.account_d1 = ''
      this.form.account_d2 = ''
      this.form.account_d3 = ''
    },
    accountD1Select() {
      this.listFiltering(1)
      this.form.account_d2 = ''
      this.form.account_d3 = ''
    },
    accountD2Select() {
      this.listFiltering(1)
      this.form.account_d3 = ''
    },
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        const from_date = this.from_date ? this.dateFormat(this.from_date) : ''
        const to_date = this.to_date ? this.dateFormat(this.to_date) : ''
        this.$emit('list-filtering', {
          ...{ page, from_date, to_date },
          ...this.form,
        })
      })
    },
    resetForm() {
      this.from_date = ''
      this.to_date = ''
      this.form.sort = ''
      this.form.account_d1 = ''
      this.form.account_d2 = ''
      this.form.account_d3 = ''
      this.form.bank_account = ''
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
