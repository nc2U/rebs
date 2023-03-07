<script lang="ts" setup>
import { numFormat, cutString } from '@/utils/baseMixins'
import { useRouter } from 'vue-router'

defineProps({
  contract: {
    type: Object,
    required: true,
  },
})

const router = useRouter()
</script>

<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>
      <router-link
        :to="{ name: '계약 등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.serial_number }}
      </router-link>
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
    <CTableDataCell>
      <router-link
        :to="{ name: '계약 등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.contractor.name }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>
      {{ !contract.last_paid_order ? '-' : contract.last_paid_order.__str__ }}
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_paid) }}
    </CTableDataCell>
    <CTableDataCell>
      <CBadge :color="contract.contractor.is_registed ? 'success' : 'danger'">
        {{ contract.contractor.is_registed ? '인가완료' : '미 인 가' }}
      </CBadge>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(contract.contractor.contractoraddress.dm_address1, 13) }}
    </CTableDataCell>
    <CTableDataCell
      >{{ contract.contractor.contractorcontact.cell_phone }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.contractor.contract_date }}</CTableDataCell>
    <CTableDataCell>
      <CButton
        type="button"
        color="success"
        size="sm"
        @click="
          router.push({
            name: '계약 등록 관리',
            query: { contract: contract.pk },
          })
        "
      >
        수정
      </CButton>
    </CTableDataCell>
  </CTableRow>
</template>
