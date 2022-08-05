<template>
  <CTableRow v-if="payment" class="text-center" :color="rowClass">
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
      <router-link to="" @click="toManage">
        {{ payment.contract ? payment.contractor : '계약정보 확인' }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link to="" @click="toManage">
        {{ numFormat(payment.income) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell
      :class="
        payment.contract && payment.installment_order === '-'
          ? 'text-danger'
          : ''
      "
    >
      {{
        payment.contract && payment.installment_order === '-'
          ? '납입회차 확인'
          : payment.installment_order
      }}
    </CTableDataCell>
    <CTableDataCell>{{ payment.bank_account }}</CTableDataCell>
    <CTableDataCell>{{ payment.trader }}</CTableDataCell>
    <CTableDataCell>
      <CButton type="button" color="info" size="sm" @click="toManage">
        확인
      </CButton>
    </CTableDataCell>
  </CTableRow>

  <FormModal ref="contMatchingModal" size="lg">
    <template #header>
      <CIcon name="cil-italic" />
      수납 건별 계약 건 매칭
    </template>
    <template #default class="p-5">
      <ContChoicer
        :payment="payment"
        @on-patch="onPatch"
        @close="$refs.contMatchingModal.visible = false"
      />
    </template>
  </FormModal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import commonMixin from '@/mixins/commonMixin'
import FormModal from '@/components/Modals/FormModal.vue'
import ContChoicer from '@/views/payments/List/components/ContChoicer.vue'

export default defineComponent({
  name: 'Payment',
  components: { FormModal, ContChoicer },
  mixins: [commonMixin],
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
  computed: {
    rowClass() {
      let cls = ''
      cls =
        this.payment.contract && this.payment.installment_order === '-'
          ? 'danger'
          : cls
      cls = !this.payment.contract ? 'warning' : cls
      return cls
    },
  },
  methods: {
    toManage() {
      return this.payment.contract ? this.toRegister() : this.contMatching()
    },
    toRegister() {
      this.$router.push({
        name: '건별수납 관리',
        query: { contract: this.payment.contract.pk, payment: this.payment.pk },
      })
    },
    contMatching(this: any) {
      if (!this.payment.contract) this.$refs.contMatchingModal.callModal()
      return
    },
    onPatch(this: any, payload: any) {
      this.$emit('on-patch', payload)
    },
  },
})
</script>
