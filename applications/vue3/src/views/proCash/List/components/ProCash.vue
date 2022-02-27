<template>
  <CTableRow class="text-center" v-if="proCash">
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ proCash.sort }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.project_account_d1 }}</CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(proCash.project_account_d2, 7) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(proCash.content, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left truncate">
      {{ cutString(proCash.trader, 7) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.bank_account, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(proCash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(proCash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.evidence }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updateConfirm" size="sm"> 수정</CButton>
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

  <FormModal size="lg" ref="updateFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 수정
    </template>
    <template v-slot:default>
      <ProCashForm
        @on-submit="updateObject"
        @close="$refs.updateFormModal.visible = false"
        :cash="cash"
      />
    </template>
  </FormModal>

  <ConfirmModal ref="delModal">
    <template v-slot:header>
      <CIcon name="cilWarning" />
      프로젝트 입출금 거래 정보 삭제
    </template>
    <template v-slot:default>
      삭제한 데이터는 복구할 수 없습니다. 해당 입출금 거래 정보를
      삭제하시겠습니까?
    </template>
    <template v-slot:footer>
      <CButton color="danger" @click="deleteObject">삭제</CButton>
    </template>
  </ConfirmModal>

  <AlertModal ref="alertModal" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import FormModal from '@/components/Modals/FormModal.vue'
import ConfirmModal from '@/components/Modals/ConfirmModal.vue'
import AlertModal from '@/components/Modals/AlertModal.vue'
import ProCashForm from '@/views/proCash/List/components/ProCashForm.vue'
import { mapGetters } from 'vuex'

export default defineComponent({
  name: 'ProCash',
  mixins: [commonMixin],
  components: { FormModal, ConfirmModal, AlertModal, ProCashForm },
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
      return this.proCash.sort
        ? scls.filter(c => c.text === this.proCash.sort).map(c => c.cls)[0]
        : ''
    },
    pageManageAuth() {
      return (
        this.superAuth ||
        (this.staffAuth && this.staffAuth.project_cash === '2')
      )
    },
    allowedPeriod(this: any) {
      return this.superAuth || this.diffDate(this.proCash.deal_date) <= 30
    },
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
    updateConfirm(this: any) {
      if (this.pageManageAuth)
        if (this.allowedPeriod) this.$refs.updateFormModal.callModal()
        else
          this.$refs.alertModal.callModal(
            null,
            '작성일로부터 30일이 경과한 기록을 수정할 수 없습니다. 관리자에게 문의하여 주십시요.',
          )
      else this.$refs.alertModal.callModal()
    },
    updateObject(this: any, payload: any) {
      this.$emit('on-update', { ...{ pk: this.proCash.pk }, ...payload })
      this.$refs.updateFormModal.visible = false
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
      this.$emit('on-delete', {
        project: this.proCash.project,
        pk: this.proCash.pk,
      })
      this.$refs.delModal.visible = false
    },
  },
})
</script>
