<script lang="ts" setup>
import { computed, ref, nextTick, watch } from 'vue'
import { numFormat } from '@/utils/baseMixins'

const props = defineProps({
  contract: {
    type: Object,
    required: true,
  },
  page: { type: Number, default: 1 },
  nowOrder: { type: Number, default: null },
  allChecked: Boolean,
})

const emit = defineEmits(['on-ctor-chk'])

const checked = ref(false)

const paidCompleted = computed(() => {
  const due: number = props.nowOrder || 2
  const last_order = props.contract.last_paid_order
  const paid: number = last_order ? last_order.pay_time : 0
  return paid >= due
})

const get_paid_name = computed(() => {
  const last_order = props.contract.last_paid_order
  return last_order ? last_order.pay_name : '계약금미납'
})

watch(props, (n, o) => {
  if (!paidCompleted.value) {
    checked.value = n.allChecked
    ctorChk(n.contract.contractor.pk)
  }
  if (n.page !== o.page) checked.value = false
})

const ctorChk = (ctorPk: string) =>
  nextTick(() => {
    emit('on-ctor-chk', { chk: checked.value, pk: ctorPk })
  })
</script>

<template>
  <CTableRow
    v-if="contract"
    class="text-center"
    :color="checked ? 'secondary' : ''"
  >
    <CTableDataCell>
      <CFormCheck
        :id="'check_' + contract.contractor.pk"
        v-model="checked"
        :value="contract.contractor.pk"
        :disabled="paidCompleted"
        label="선택"
        @change="ctorChk(contract.contractor.pk)"
      />
    </CTableDataCell>

    <CTableDataCell>
      {{ contract.order_group_desc.order_group_name }}
    </CTableDataCell>

    <CTableDataCell class="text-left">
      <CIcon
        name="cibDiscover"
        :style="'color:' + contract.unit_type_desc.color"
        size="sm"
        class="mr-1"
      />
      {{ contract.unit_type_desc.name }}
    </CTableDataCell>
    <CTableDataCell>
      {{ contract.serial_number }}
    </CTableDataCell>
    <CTableDataCell
      :class="contract.keyunit.houseunit ? '' : 'text-danger'"
      class="text-left"
    >
      {{
        contract.keyunit.houseunit ? contract.keyunit.houseunit.__str__ : '미정'
      }}
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약 등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.contractor.name }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link
        :to="{ name: '건별 수납 관리', query: { contract: contract.pk } }"
      >
        {{ numFormat(contract.total_paid) }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      <span v-if="paidCompleted" class="text-success">완납중</span>
      <span v-else class="text-danger">미납중</span>
      ({{ get_paid_name }})
    </CTableDataCell>
    <CTableDataCell>{{ contract.contractor.contract_date }}</CTableDataCell>
  </CTableRow>
</template>
