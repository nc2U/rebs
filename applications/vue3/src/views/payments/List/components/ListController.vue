<template>
  <CCallout color="success" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <CFormInput
              v-model="form.from_date"
              @keydown.enter="payFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="수납일자(From)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormInput
              v-model="form.to_date"
              @keydown.enter="payFiltering(1)"
              v-maska="'####-##-##'"
              placeholder="수납일자(To)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_order" @change="payFiltering(1)">
              <option value="">납부회차 선택</option>
              <option v-for="po in payOrderList" :value="po.pk" :key="po.pk">
                {{ po.__str__ }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_account" @change="payFiltering(1)">
              <option value="">납부계좌 선택</option>
              <option
                v-for="ba in pBankAccountList"
                :value="ba.pk"
                :key="ba.pk"
              >
                {{ ba.alias_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol lg="5">
        <CRow>
          <CCol md="6" class="mb-3 pl-4 pt-2 text-center">
            <CFormSwitch
              v-model="form.is_unRegisted"
              label="미등록 수납대금만 보기"
            />
          </CCol>

          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                @keydown.enter="payFiltering(1)"
                placeholder="계약자, 입금자, 비고"
                aria-label="Username"
                aria-describedby="addon-wrapping"
              />
              <CInputGroupText @click="payFiltering(1)">검색</CInputGroupText>
            </CInputGroup>
          </CCol>
        </CRow>
      </CCol>
    </CRow>
    <!--    <CAlert color="default">-->
    <!--      <CRow>-->
    <!--        <CCol v-if="contractsCount > 0" class="pt-1">-->
    <!--          해당 조건 계약 건수 : {{ contractsCount }} 건-->
    <!--        </CCol>-->
    <!--        <CCol class="text-right mb-0" v-if="!formsCheck">-->
    <!--          <CButton color="info" @click="resetForm" size="sm" class="m-0">-->
    <!--            검색조건 초기화-->
    <!--          </CButton>-->
    <!--        </CCol>-->
    <!--      </CRow>-->
    <!--    </CAlert>-->
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
        pay_order: '',
        pay_account: '',
        is_unRegisted: '',
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
      const e = this.form.is_unRegisted === ''
      const f = this.form.search === ''
      return a && b && c && d && e && f
    },
    ...mapState('cash', ['payOrderList', 'pBankAccountList']),
  },
  methods: {
    payFiltering(page = 1) {
      this.$nextTick(() => {
        this.$emit('pay-filtering', { ...{ page }, ...this.form })
      })
    },
    resetForm() {
      this.form.from_date = ''
      this.form.to_date = ''
      this.form.pay_order = ''
      this.form.pay_account = ''
      this.form.is_unRegisted = ''
      this.form.search = ''
      this.payFiltering(1)
    },
  },
})
</script>
