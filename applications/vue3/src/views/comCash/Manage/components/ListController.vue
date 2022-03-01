<template>
  <CCallout color="primary" class="pb-0 mb-4">
    <CRow>
      <CCol lg="3">
        <CRow>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="from_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
            />
          </CCol>
          <CCol md="6" class="mb-3">
            <DatePicker
              v-model="to_date"
              @keydown.enter="listFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
            />
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="5">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="sort" @change="sortSelect">
              <option value="">구분</option>
              <option value="1">입금</option>
              <option value="2">출금</option>
              <option value="3">대체</option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="account_d1" @change="accountD1Select">
              <option value="">계정[대분류]</option>
              <option
                v-for="acc1 in formAccD1List"
                :value="acc1.pk"
                :key="acc1.pk"
              >
                {{ acc1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="account_d2"
              @change="accountD2Select"
              :disabled="!this.account_d1"
            >
              <option value="">계정[중분류]</option>
              <option
                v-for="acc2 in formAccD2List"
                :value="acc2.pk"
                :key="acc2.pk"
              >
                {{ acc2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect
              v-model="account_d3"
              @change="listFiltering(1)"
              :disabled="!this.account_d1"
            >
              <option value="">계정[소분류]</option>
              <option
                v-for="acc3 in formAccD3List"
                :value="acc3.pk"
                :key="acc3.pk"
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
            <CFormSelect v-model="bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option v-for="acc in comBankList" :value="acc.pk" :key="acc.pk">
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="8" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="search"
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
      sort: '',
      account_d1: '',
      account_d2: '',
      account_d3: '',
      bank_account: '',
      search: '',
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.from_date === ''
      const b = this.to_date === ''
      const c = this.sort === ''
      const d = this.account_d1 === ''
      const e = this.account_d2 === ''
      const f = this.account_d3 === ''
      const g = this.bank_account === ''
      const h = this.search === ''
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
      this.account_d1 = ''
      this.account_d2 = ''
      this.account_d3 = ''
    },
    accountD1Select() {
      this.listFiltering(1)
      this.account_d2 = ''
      this.account_d3 = ''
    },
    accountD2Select() {
      this.listFiltering(1)
      this.account_d3 = ''
    },
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        this.from_date = this.from_date ? this.dateFormat(this.from_date) : ''
        this.to_date = this.to_date ? this.dateFormat(this.to_date) : ''
        this.$emit('list-filtering', { ...{ page }, ...this })
      })
    },
    resetForm() {
      this.from_date = ''
      this.to_date = ''
      this.sort = ''
      this.account_d1 = ''
      this.account_d2 = ''
      this.account_d3 = ''
      this.bank_account = ''
      this.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
