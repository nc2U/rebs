<template>
  <CCallout color="success" class="pb-0 mb-3">
    <CRow>
      <CCol lg="9">
        <CRow>
          <CCol md="6" lg="2" class="mb-3">
            <DatePicker
              v-model="from_date"
              v-maska="'####-##-##'"
              placeholder="시작일 (From)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <DatePicker
              v-model="to_date"
              v-maska="'####-##-##'"
              placeholder="종료일 (To)"
              @keydown.enter="listFiltering(1)"
            />
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.sort" @change="pro_acc_d1Select">
              <option value="">거래구분</option>
              <option v-for="sort in sortList" :key="sort.pk" :value="sort.pk">
                {{ sort.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d1" @change="pro_acc_d2Select">
              <option value="">상위 항목</option>
              <option v-for="d1 in formAccD1List" :key="d1.pk" :value="d1.pk">
                {{ d1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d2" @change="listFiltering(1)">
              <option value="">하위 항목</option>
              <option v-for="d2 in formAccD2List" :key="d2.pk" :value="d2.pk">
                {{ d2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option
                v-for="acc in imprestBAccount"
                :key="acc.pk"
                :value="acc.pk"
              >
                {{ acc.alias_name }}
              </option>
            </CFormSelect>
          </CCol>
        </CRow>
      </CCol>

      <CCol lg="3">
        <CRow>
          <CCol class="mb-3">
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
          거래 건수 조회 결과 : {{ numFormat(proImprestCount) }} 건
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
import { mapGetters, mapState } from 'vuex'

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
        pro_acc_d1: '',
        pro_acc_d2: '',
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
      const d = this.form.pro_acc_d1 === ''
      const e = this.form.pro_acc_d2 === ''
      const f = this.form.bank_account === ''
      const g = this.form.search === ''
      return a && b && c && d && e && f && g
    },
    ...mapState('proCash', [
      'sortList',
      'formAccD1List',
      'formAccD2List',
      'proImprestCount',
    ]),
    ...mapGetters('proCash', ['imprestBAccount']),
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
    pro_acc_d1Select() {
      this.listFiltering(1)
      this.form.pro_acc_d1 = ''
      this.form.pro_acc_d2 = ''
    },
    pro_acc_d2Select() {
      this.listFiltering(1)
      this.form.pro_acc_d2 = ''
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
      this.form.pro_acc_d1 = ''
      this.form.pro_acc_d2 = ''
      this.form.bank_account = ''
      this.form.search = ''
      this.listFiltering(1)
    },
  },
})
</script>
