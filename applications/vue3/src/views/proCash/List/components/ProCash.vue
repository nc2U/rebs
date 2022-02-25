<template>
  <CTableRow class="text-center" v-if="proCash">
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ proCash.cash_category1 }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.project_account_d1 }}</CTableDataCell>
    <CTableDataCell class="text-left truncate"
      >{{ cutString(proCash.project_account_d2, 7) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(proCash.content, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(proCash.trader, 7) }}
    </CTableDataCell>
    <CTableDataCell class="text-left"
      >{{ cutString(proCash.bank_account, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(proCash.income) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(proCash.outlay) }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.evidence }}</CTableDataCell>
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
    sortClass() {
      const scls = [
        { text: '입금', cls: 'text-primary' },
        { text: '출금', cls: 'text-danger' },
        { text: '대체', cls: 'text-info' },
      ]
      return this.proCash.cash_category1
        ? scls
            .filter((c: any) => c.text === this.proCash.cash_category1)
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
