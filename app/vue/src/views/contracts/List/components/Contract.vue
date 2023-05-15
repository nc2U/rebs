<script lang="ts" setup>
import { computed } from 'vue'
import { numFormat } from '@/utils/baseMixins'
import { useRouter } from 'vue-router'

const props = defineProps({
  contract: {
    type: Object,
    required: true,
  },
})

const contractor = computed(() => props.contract.contractor.pk)

const router = useRouter()
</script>

<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>
      <router-link :to="{ name: '계약 등록 관리', query: { contractor } }">
        {{ contract.serial_number }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      <router-link :to="{ name: '계약 등록 관리', query: { contractor } }">
        {{ contract.contractor.name }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      <CBadge :color="contract.contractor.is_registed ? 'success' : 'danger'">
        {{ contract.contractor.is_registed ? '인가완료' : '미 인 가' }}
      </CBadge>
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
    <CTableDataCell
      class="text-left"
      :class="contract.keyunit.houseunit !== null ? '' : 'text-danger'"
    >
      {{
        contract.keyunit.houseunit ? contract.keyunit.houseunit.__str__ : '미정'
      }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.contractor.contract_date }}</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.contractprice?.price || 0) }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.contractprice?.down_pay || 0) }}
    </CTableDataCell>
    <CTableDataCell>
      {{ !contract.last_paid_order ? '-' : contract.last_paid_order.__str__ }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_paid) }}
    </CTableDataCell>
    <CTableDataCell
      >{{ contract.contractor.contractorcontact.cell_phone }}
    </CTableDataCell>
    <CTableDataCell>
      <CButton
        type="button"
        color="success"
        size="sm"
        @click="
          router.push({
            name: '계약 등록 관리',
            query: { contractor },
          })
        "
      >
        수정
      </CButton>
    </CTableDataCell>
  </CTableRow>
</template>
