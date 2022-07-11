<template>
  <CTableRow v-if="contract" class="text-center">
    <CTableDataCell>
      <CFormCheck
        :id="contract.constructor.pk"
        name="chk[]"
        :value="contract.constructor.pk"
        label="선택"
      />
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.serial_number }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell>{{ contract.order_group.order_group_name }}</CTableDataCell>
    <CTableDataCell class="text-left">
      <CIcon
        name="cibDiscover"
        :style="'color:' + contract.type_color"
        size="sm"
        class="mr-1"
      />
      {{ contract.unit_type }}
    </CTableDataCell>
    <CTableDataCell
      class="text-left"
      :class="contract.house_unit === '[미정]' ? 'text-danger' : ''"
    >
      {{ contract.house_unit }}
    </CTableDataCell>
    <CTableDataCell>
      <router-link
        :to="{ name: '계약등록 관리', query: { contract: contract.pk } }"
      >
        {{ contract.contractor }}
      </router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_paid) }}
    </CTableDataCell>
    <CTableDataCell>
      {{
        contract.last_paid_order === '-'
          ? '-'
          : contract.last_paid_order.__str__
      }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Contract',
  components: {},

  props: {
    contract: {
      type: Object,
      required: true,
    },
  },
})
</script>
