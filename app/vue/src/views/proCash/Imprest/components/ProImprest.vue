<template>
  <CTableRow
    class="text-center"
    :color="rowColor"
    v-if="imprest"
    :style="imprest.is_separate ? 'font-weight: bold;' : ''"
  >
    <CTableDataCell>{{ imprest.deal_date }}</CTableDataCell>
    <CTableDataCell :class="sortClass">
      {{ imprest.sort_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ imprest.project_account_d1_desc }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.project_account_d2_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.content, 10) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.trader, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(imprest.bank_account_desc, 9) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="success">
      {{ numFormat(imprest.income || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right" color="danger">
      {{ numFormat(imprest.outlay || 0) }}
    </CTableDataCell>
    <CTableDataCell>{{ imprest.evidence_desc }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="info" @click="showDetail" size="sm">확인</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal size="lg" ref="updateFormModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      운영비(전도금) 거래 건별 관리
    </template>
    <template v-slot:default>
      <ProImprestForm
        @multi-submit="multiSubmit"
        @on-delete="onDelete"
        @close="$refs.updateFormModal.visible = false"
        :imprest="imprest"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import FormModal from '@/components/Modals/FormModal.vue'
import ProImprestForm from '@/views/proCash/Imprest/components/ProImprestForm.vue'

export default defineComponent({
  name: 'ProImprest',
  mixins: [commonMixin],
  components: { FormModal, ProImprestForm },
  props: {
    imprest: {
      type: Object,
      required: true,
    },
  },
  computed: {
    sortClass() {
      const cls = ['', 'text-primary', 'text-danger', 'text-info']
      return cls[this.imprest.sort]
    },
    rowColor() {
      let color = ''
      color =
        this.imprest.contract && this.imprest.project_account_d2 <= '2'
          ? 'info'
          : color
      color = this.imprest.is_separate ? 'dark' : color
      color = this.imprest.separated ? 'primary' : color
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
