<template>
  <CTableRow
    class="text-center"
    :color="rowColor"
    v-if="proCash"
    :style="proCash.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ proCash.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ proCash.sort_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ proCash.project_account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.project_account_d2_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.trader, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(proCash.bank_account_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(proCash.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(proCash.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ proCash.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" @click="showDetail" size="sm">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal size="lg" ref="updateFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      프로젝트 입출금 거래 건별 관리
    </template>
    <template v-slot:default>
      <ProCashForm
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="$refs.updateFormModal.visible = false"
        :pro-cash="proCash"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import FormModal from '@/components/Modals/FormModal.vue'
import ProCashForm from '@/views/proCash/Manage/components/ProCashForm.vue'

export default defineComponent({
  name: 'ProCash',
  mixins: [commonMixin],
  components: { FormModal, ProCashForm },
  props: {
    proCash: {
      type: Object,
      required: true,
    },
  },
  computed: {
    sortClass() {
      const cls = ['', 'text-primary', 'text-danger', 'text-info']
      return cls[this.proCash.sort]
    },
    rowColor() {
      let color = ''
      color =
        this.proCash.contract && this.proCash.project_account_d2 <= '2'
          ? 'info'
          : color
      color = this.proCash.is_separate ? 'primary' : color
      color = this.proCash.separated ? 'secondary' : color
      return color
    },
  },
  methods: {
    showDetail(this: any) {
      this.$refs.updateFormModal.callModal()
    },
    // onCreate(payload: any) {
    //   this.$emit('on-create', payload)
    // },
    // onUpdate(payload: any) {
    //   this.$emit('on-update', payload)
    // },
    multiSubmit(payload: any) {
      this.$emit('multi-submit', payload)
    },
    onDelete(payload: any) {
      this.$emit('on-delete', payload)
    },
  },
})
</script>
