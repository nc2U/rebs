<template>
  <CCallout color="warning" class="pb-0 mb-4">
    <CRow>
      <CCol lg="7">
        <CRow>
          <CCol md="6" lg="3" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="납부일자 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="납부일자 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_order" @change="listFiltering(1)">
              <option value="">납부회차 선택</option>
              <option v-for="po in payOrderList" :key="po.pk" :value="po.pk">
                {{ po.__str__ }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="3" class="mb-3">
            <CFormSelect v-model="form.pay_account" @change="listFiltering(1)">
              <option value="">납부계좌 선택</option>
              <option
                v-for="ba in proBankAccountList"
                :key="ba.pk"
                :value="ba.pk"
              >
                {{ ba.alias_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>
      <CCol lg="5">
        <CRow>
          <CCol md="6" class="mb-3 pl-4 pt-2">
            <CFormSwitch
              id="no_contract"
              v-model="form.no_contract"
              label="미등록 납부대금 건"
              @change="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" class="mb-3">
            <CInputGroup class="flex-nowrap">
              <CFormInput
                v-model="form.search"
                placeholder="계약자, 입금자, 적요, 비고"
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
        <strong>납부 건수 조회 결과 : {{ paymentsCount }} 건</strong>
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
        pay_order: '',
        pay_account: '',
        no_contract: false,
        search: '',
      },
    }
  },
  computed: {
    formsCheck(this: any) {
      const a = this.from_date === ''
      const b = this.to_date === ''
      const c = this.form.pay_order === ''
      const d = this.form.pay_account === ''
      const e = !this.form.no_contract
      const f = this.form.search === ''
      return a && b && c && d && e && f
    },
    ...mapState('payment', ['payOrderList', 'paymentsCount']),
    ...mapState('proCash', ['proBankAccountList']),
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
    listFiltering(this: any, page = 1) {
      this.$nextTick(() => {
        const from_date = this.from_date ? this.dateFormat(this.from_date) : ''
        const to_date = this.to_date ? this.dateFormat(this.to_date) : ''
        this.$emit('payment-filtering', {
          ...{ page, from_date, to_date },
          ...this.form,
        })
      })
    },
    resetForm() {
      this.from_date = ''
      this.to_date = ''
      this.form.pay_order = ''
      this.form.pay_account = ''
      this.form.no_contract = false
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
