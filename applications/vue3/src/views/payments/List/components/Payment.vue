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
        :to="
          payment.contract
            ? {
                name: '건별수납 관리',
                query: { contract: payment.contract.pk, payment: payment.pk },
              }
            : { name: '건별수납 관리', query: { payment: payment.pk } }
        "
      >
        {{ payment.contract ? payment.contractor : '계약정보 확인' }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link
        :to="
          payment.contract
            ? {
                name: '건별수납 관리',
                query: { contract: payment.contract.pk, payment: payment.pk },
              }
            : {
                name: '건별수납 관리',
                query: { payment: payment.pk },
              }
        "
      >
        {{ numFormat(payment.income) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ payment.installment_order }}</CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" @click="updatePayment" size="sm"> 수정</CButton>
      <CButton color="danger" @click="deletePayment" size="sm"> 삭제</CButton>
    </CTableDataCell>
  </CTableRow>

  <ConfirmModal ref="confirmModal">
    <template v-slot:header>
      <CIcon name="cil-italic" />
      납입대금 건별 수정
    </template>
    <template v-slot:default>
      해당 납입대금 정보 수정 등록을 진행하시겠습니까?
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
  name: 'Payment',
  mixins: [commonMixin],
  components: { ConfirmModal, AlertModal },
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters('accounts', ['staffAuth', 'superAuth']),
  },
  methods: {
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
