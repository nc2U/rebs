<template>
  <CTableRow class="text-center" v-if="cash">
    <CTableDataCell>{{ cash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ cash.cash_category1 }}
    </CTableDataCell>
    <CTableDataCell>{{ cash.cash_category2 }}</CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cash.account }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.content, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.trader, 7) }}
    </CTableDataCell>
    <CTableDataCell class="text-left"
      >{{ cutString(cash.bank_account, 9) }}
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
  props: {
    cash: {
      type: Object,
      required: true,
    },
  },
  computed: {
    sortClass() {
      const scls = [
        { text: '입금', cls: 'text-primary' },
        { text: '출금', cls: 'text-danger' },
        { text: '대체', cls: 'text-info' },
      ]
      return this.cash.cash_category1
        ? scls
            .filter((c: any) => c.text === this.cash.cash_category1)
            .map((c: any) => c.cls)[0]
        : ''
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
