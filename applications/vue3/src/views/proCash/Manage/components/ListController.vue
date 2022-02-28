<template>
  <CCallout color="success" class="pb-0 mb-3">
    <CRow>
      <CCol lg="9">
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
            <CFormSelect v-model="form.sort" @change="pro_acc_d1Select">
              <option value="">거래구분</option>
              <option v-for="sort in sortList" :value="sort.pk" :key="sort.pk">
                {{ sort.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d1" @change="pro_acc_d2Select">
              <option value="">상위 항목</option>
              <option v-for="d1 in formAccD1List" :value="d1.pk" :key="d1.pk">
                {{ d1.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.pro_acc_d2" @change="listFiltering(1)">
              <option value="">하위 항목</option>
              <option v-for="d2 in formAccD2List" :value="d2.pk" :key="d2.pk">
                {{ d2.name }}
              </option>
            </CFormSelect>
          </CCol>

          <CCol md="6" lg="2" class="mb-3">
            <CFormSelect v-model="form.bank_account" @change="listFiltering(1)">
              <option value="">거래계좌</option>
              <option
                v-for="acc in proBankAccountList"
                :value="acc.pk"
                :key="acc.pk"
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
          거래 건수 조회 결과 : {{ numFormat(proCashesCount) }} 건
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
      const a = this.form.from_date === ''
      const b = this.form.to_date === ''
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
      'proBankAccountList',
      'proCashesCount',
    ]),
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
    listFiltering(page = 1) {
      this.$nextTick(() =>
        this.$emit('list-filtering', { ...{ page }, ...this.form }),
      )
    },
    resetForm() {
      this.form.from_date = ''
      this.form.to_date = ''
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
