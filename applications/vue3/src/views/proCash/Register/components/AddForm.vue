<template>
  <CTableRow>
    <CTableDataCell>
      <CFormSelect v-model="form.sort">
        <option value="">---------</option>
        <option value="1">입금</option>
        <option value="2">출금</option>
        <option value="3">대체</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d1">
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.account_d2">
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.content" placeholder="적요" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.trader" placeholder="거래처" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.bank_account">
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.income" type="number" placeholder="입금액" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.outlay" type="number" placeholder="출금액" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect v-model="form.evidence">
        <option value="">---------</option>
      </CFormSelect>
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput v-model="form.note" placeholder="비고" />
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapActions } from 'vuex'

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
  computed: {},
  methods: {
    ...mapActions('proCash', [
      'fetchProFormAccD1List',
      'fetchProFormAccD2List',
    ]),
  },
})
</script>
