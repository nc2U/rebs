<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ cash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ cash.sort }}
    </CTableDataCell>
    <CTableDataCell :class="d1Class">
      {{ cash.account_d1 }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cash.account_d3 }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.trader, 8) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(cash.bank_account, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="primary">
      {{ numFormat(cash.income) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(cash.outlay) }}
    </CTableDataCell>
    <CTableDataCell>{{ cash.evidence }}</CTableDataCell>
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
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Cashes',
  components: { ConfirmModal, AlertModal },
  data() {
    return {
      cls: ['text-primary', 'text-danger', 'text-info'],
    }
  },
  props: {
    cash: {
      type: Object,
      required: true,
    },
  },
  computed: {
    sortClass(this: any) {
      const sort = ['입금', '출금', '대체']
      return this.cls[sort.indexOf(this.cash.sort)]
    },
    d1Class() {
      const d1 = ['수익', '비용', '대체']
      return this.cls[d1.indexOf(this.cash.account_d1)]
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    cutString(str: string, len: number) {
      const content = str ? str : ''
      return content.length > len ? `${content.substr(0, len)}..` : content
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
