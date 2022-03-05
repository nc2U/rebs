<template>
  <CTableRow
    class="text-center"
    v-if="payment"
    :color="payment.contract ? '' : 'warning'"
  >
    <CTableDataCell>{{ payment.deal_date }}</CTableDataCell>
    <CTableDataCell>{{ payment.order_group }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CIcon
        v-if="payment.contract"
        name="cib-node-js"
        :style="{ color: payment.type_color }"
        size="sm"
        class="mr-1"
      />
      {{ payment.type_name }}
    </CTableDataCell>
    <CTableDataCell>{{ payment.serial_number }}</CTableDataCell>
    <CTableDataCell>
      <router-link
        @click="contMatching"
        :to="
          payment.contract
            ? {
                name: '건별수납 관리',
                query: { contract: payment.contract.pk, payment: payment.pk },
              }
            : ''
        "
      >
        {{ payment.contract ? payment.contractor : '계약정보 확인' }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link
        @click="contMatching"
        :to="
          payment.contract
            ? {
                name: '건별수납 관리',
                query: { contract: payment.contract.pk, payment: payment.pk },
              }
            : ''
        "
      >
        {{ numFormat(payment.income) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      {{ payment.installment_order }}
    </CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updatePayment" size="sm"> 수정</CButton>
      <CButton color="danger" @click="deletePayment" size="sm"> 삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal size="lg" ref="contMatchingModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      수납 건별 계약 건 매칭
    </template>
    <template v-slot:default class="p-5">
      <ContChoicer
        :payment="payment"
        @close="$refs.contMatchingModal.visible = false"
      />
    </template>
  </FormModal>

  <!--  <AlertModal ref="alertModal" />-->
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/views/commonMixin'
import FormModal from '@/components/Modals/FormModal.vue'
import ContChoicer from '@/views/payments/List/components/ContChoicer.vue'
// import AlertModal from '@/components/Modals/AlertModal.vue'

export default defineComponent({
  name: 'Payment',
  mixins: [commonMixin],
  components: { FormModal, ContChoicer },
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
  methods: {
    contMatching(this: any) {
      if (!this.payment.contract) this.$refs.contMatchingModal.callModal()
      return
    },
    updatePayment(this: any) {
      this.$emit('on-update', { ...{ pk: this.payment.pk }, ...this.form })
    },
    deletePayment(this: any) {
      this.$emit('on-delete', this.payment.pk)
    },
  },
})
</script>
