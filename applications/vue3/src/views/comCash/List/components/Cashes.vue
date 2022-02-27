<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ cash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ cash.sort_desc }}
    </CTableDataCell>
    <CTableDataCell :class="d1Class">
      {{ cash.account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cash.account_d3_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(cash.trader, 8) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(cash.bank_account_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="primary">
      {{ numFormat(cash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(cash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ cash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton
        color="success"
        @click="updateConfirm"
        size="sm"
        :disabled="!pageManageAuth || !allowedPeriod"
      >
        수정
      </CButton>
      <CButton
        color="danger"
        @click="deleteConfirm"
        size="sm"
        :disabled="!pageManageAuth || !allowedPeriod"
      >
        삭제
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal size="lg" ref="cashUpdateModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      입출금 거래 건별 수정
    </template>
    <template v-slot:default>
      <CashForm
        @on-submit="updateObject"
        @close="$refs.cashUpdateModal.visible = false"
        :cash="cash"
      />
    </template>
  </FormModal>

  <ConfirmModal ref="delModal">
    <template v-slot:header>
      <CIcon name="cilWarning" />
      입출금 거래 정보 삭제
    </template>
    <template v-slot:default>
      해당 입출금 거래 건별 정보 삭제를 진행합니다.
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import FormModal from '@/components/Modals/FormModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import CashForm from '@/views/comCash/List/components/CashForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'Cashes',
  components: { FormModal, ConfirmModal, AlertModal, CashForm },
  props: {
    cash: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      cls: ['text-primary', 'text-danger', 'text-info'],
    }
  },
  computed: {
    sortClass(this: any) {
      return this.cls[this.cash.sort - 1]
    },
    d1Class() {
      return this.cls[this.cash.account_d1 - 4]
    },
    pageManageAuth() {
      return (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.company_cash === '2')
      )
    },
    allowedPeriod() {
      return this.superAuth || this.diffDate(this.cash.deal_date) <= 30
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    cutString(str: string, len: number) {
      const content = str ? str : ''
      return content.length > len ? `${content.substr(0, len)}..` : content
    },
    updateConfirm(this: any) {
      if (this.pageManageAuth) {
        if (this.allowedPeriod) this.$refs.cashUpdateModal.callModal()
        else
          this.$refs.alertModal.callModal(
            null,
            '작성일로부터 30일이 경과한 기록을 수정할 수 없습니다. 관리자에게 문의하여 주십시요.',
          )
      } else this.$refs.alertModal.callModal()
    },
    updateObject(this: any, payload: any) {
      this.$emit('on-update', { ...{ pk: this.cash.pk }, ...payload })
      this.$refs.cashUpdateModal.visible = false
    },
    deleteConfirm(this: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.$refs.delModal.callModal()
        else
          this.$refs.alertModal.callModal(
            null,
            '작성일로부터 30일이 경과한 기록을 삭제할 수 없습니다. 관리자에게 문의하여 주십시요.',
          )
      else this.$refs.alertModal.callModal()
    },

    deleteObject(this: any) {
      this.$emit('on-delete', { company: this.cash.company, pk: this.cash.pk })
      this.$refs.delModal.visible = false
    },

    diffDate(date: string) {
      const now = new Date()
      const start = new Date(date)
      const btween = now.getTime() - start.getTime()
      return btween / 1000 / 60 / 60 / 24
    },
  },
})
</script>
