<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.sort" @change="sort_change">
        <option value="">---------</option>
        <option value="1">입금</option>
        <option value="2">출금</option>
        <option value="3">대체</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d1" @change="d1_change">
        <option value="">---------</option>
        <option
            v-for="d1 in formAccD1List"
            :value="d1.pk"
            :key="d1.pk"
        >
          {{ d1.name }}
        </option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d2">
        <option value="">---------</option>
        <option v-for="d2 in formAccD2List" :value="d2.pk" :key="d2.pk">{{ d2.name }}</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.content" placeholder="적요"/>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.trader" placeholder="거래처"/>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.bank_account">
        <option value="">---------</option>
        <option v-for="ba in proBankAccountList" :value="ba.pk" :key="ba.pk">{{ ba.alias_name }}</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.income" type="number" min="0" placeholder="입금액"/>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.outlay" type="number" min="0" placeholder="출금액"/>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.evidence">
        <option value="">---------</option>
        <option value="1">세금계산서</option>
        <option value="2">계산서(면세)</option>
        <option value="3">신용카드전표</option>
        <option value="4">현금영수증</option>
        <option value="5">간이영수증</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.note" placeholder="비고"/>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import {defineComponent} from 'vue'
import {mapActions, mapState} from 'vuex'

export default defineComponent({
  name: 'AddForm',
  props: {},
  setup() {
    return {}
  },
  data() {
    return {
      form: {
        sort: '',
        account_d1: '',
        account_d2: '',
        content: '',
        trader: '',
        bank_account: '',
        income: '',
        outlay: '',
        evidence: '',
        note: '',
      },
    }
  },
  computed: {
    ...mapState('proCash', [
      'formAccD1List',
      'formAccD2List',
      'proBankAccountList'
    ]),
  },
  methods: {
    sort_change() {
      this.$nextTick(() => this.fetchProFormAccD1List(this.form.sort))
    },
    d1_change() {
      this.$nextTick(() => this.fetchProFormAccD2List({d1: this.form.account_d1, sort: this.form.sort}))
    },
    ...mapActions('proCash', [
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
    ]),
  },
})
</script>
