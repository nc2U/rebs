<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="`text-${getSort(proCash.cash_category1).cls}`">
      {{ getSort(proCash.cash_category1).val }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.project_account_d1 }}</CTableDataCell>
    <CTableDataCell>{{ proCash.project_account_d2 }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ proCash.content }}</CTableDataCell>
    <CTableDataCell class="text-left">{{ proCash.trader }}</CTableDataCell>
    <CTableDataCell>{{ proCash.bank_account }}</CTableDataCell>
    <CTableDataCell class="text-right" color="primary">
      {{ numFormat(proCash.income) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(proCash.outlay) }}
    </CTableDataCell>
    <CTableDataCell>{{ getEvidence(proCash.evidence) }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updatePayment" size="sm"> 수정</CButton>
      <CButton color="danger" @click="deletePayment" size="sm"> 삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 수정
    </template>
    <template v-slot:default>
      해당 입출금거래 정보 수정 등록을 진행하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="primary" @click="modalAction">저장</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProCash',
  mixins: [commonMixin],
  components: { ConfirmModal, AlertModal },
  props: {
    proCash: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    getSort(val: string) {
      const sort = [
        { key: '1', val: '입금', cls: 'primary' },
        { key: '2', val: '출금', cls: 'danger' },
        { key: '3', val: '대체', cls: 'info' },
      ]
      return sort.filter((s: any) => s.key === val)[0]
    },
    getEvidence(val: string) {
      const evidence = [
        { key: '0', val: '증빙 없음' },
        { key: '1', val: '세금계산서' },
        { key: '2', val: '계산서(면세)' },
        { key: '3', val: '신용카드전표' },
        { key: '4', val: '현금영수증' },
        { key: '5', val: '간이영수증' },
      ]
      return evidence
        .filter((e: any) => e.key === val)
        .map((e: any) => e.val)[0]
    },
    updatePayment(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.payment === '2'))
        this.$emit('on-update', { ...{ pk: this.payment.pk }, ...this.form })
      else this.$refs.alertModal.callModal()
    },
    deletePayment(this: any) {
      if (this.superAuth || (this.staffAuth && this.staffAuth.payment === '2'))
        this.$emit('on-delete', this.payment.pk)
      else this.$refs.alertModal.callModal()
    },
  },
})
</script>
