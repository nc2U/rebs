<template>
  <CCallout color="warning" class="pb-0 mb-4">
    <CRow>
      <CCol>
        <CRow>
          <CFormLabel class="col-sm-1 col-form-label">타입</CFormLabel>
          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_order" @change="listFiltering(1)">
              <option value="">타입 선택</option>
              <option v-for="po in payOrderList" :value="po.pk" :key="po.pk">
                {{ po.__str__ }}
              </option>
            </CFormSelect>
          </CCol>

          <CFormLabel class="col-sm-1 col-form-label">계약자</CFormLabel>
          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_account" @change="listFiltering(1)">
              <option value="">계약자 선택</option>
              <option
                v-for="ba in pBankAccountList"
                :value="ba.pk"
                :key="ba.pk"
              >
                {{ ba.alias_name }}
              </option>
            </CFormSelect>
          </CCol>

          <CFormLabel class="col-sm-1 col-form-label">검색</CFormLabel>
          <CCol md="3" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                @keydown.enter="listFiltering(1)"
                placeholder="계약자, 입금자, 적요, 비고"
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
        <strong>납부 건수 조회 결과 : 0건</strong>
      </CCol>
      <!--      <CCol class="text-right mb-0" v-if="!formsCheck">-->
      <!--        <CButton color="info" @click="resetForm" size="sm">-->
      <!--          검색조건 초기화-->
      <!--        </CButton>-->
      <!--      </CCol>-->
    </CRow>
  </CCallout>

  <CAlert color="info"></CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { maska } from 'maska'
import { mapState } from 'vuex'

export default defineComponent({
  name: 'ListController',
  components: {},

  directives: { maska },
  data() {
    return {
      form: {
        from_date: '',
        to_date: '',
        pay_order: '',
        pay_account: '',
        no_contract: false,
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.form.from_date === ''
      const b = this.form.to_date === ''
      const c = this.form.pay_order === ''
      const d = this.form.pay_account === ''
      const e = !this.form.no_contract
      const f = this.form.search === ''
      return a && b && c && d && e && f
    },
    ...mapState('payment', [
      'payOrderList',
      'pBankAccountList',
      'paymentsCount',
    ]),
  },
  methods: {
    listFiltering(page = 1) {
      this.$nextTick(() =>
        this.$emit('payment-filtering', { ...{ page }, ...this.form }),
      )
    },
    resetForm() {
      this.form.from_date = ''
      this.form.to_date = ''
      this.form.pay_order = ''
      this.form.pay_account = ''
      this.form.no_contract = false
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
