<script lang="ts" setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { numFormat } from '@/utils/baseMixins'

const props = defineProps({
  payment: {
    type: Object,
    required: true,
  },
})

const router = useRouter()
const contMatchingModal = ref()

const rowClass = computed(() => {
  let cls = ''
  cls =
    props.payment.contract && props.payment.installment_order === '-'
      ? 'danger'
      : cls
  cls = !props.payment.contract ? 'warning' : cls
  return cls
})

const toManage = () => (props.payment.contract ? toRegister() : contMatching())
const toRegister = () => {
  router.push({
    name: '건별수납 관리',
    query: { contract: props.payment.contract.pk, payment: props.payment.pk },
  })
}
const contMatching = () => {
  if (!props.payment.contract) contMatchingModal.value.callModal()
  return
}
</script>

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
</template>
