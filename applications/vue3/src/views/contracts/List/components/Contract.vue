<template>
  <CTableRow v-if="contract">
    <CTableDataCell>
      <router-link to="#">{{ contract.serial_number }}</router-link>
    </CTableDataCell>
    <CTableDataCell>{{ contract.order_group }}</CTableDataCell>
    <CTableDataCell>
      <CIcon
        name="cibDiscover"
        :style="'color:' + contract.type_color"
        size="sm"
      />&nbsp;
      {{ contract.unit_type }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.house_unit }}</CTableDataCell>
    <CTableDataCell>
      <router-link to="#">{{ contract.contractor }}</router-link>
    </CTableDataCell>
    <CTableDataCell>
      <CBadge :color="contract.is_registed ? 'success' : 'danger'">
        {{ contract.is_registed ? '인가완료' : '미 인 가' }}
      </CBadge>
    </CTableDataCell>
    <CTableDataCell>{{ contract.address }}</CTableDataCell>
    <CTableDataCell>{{ contract.cell_phone }}</CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Contract',
  props: {
    contract: {
      type: Object,
      required: true,
    },
  },
})
</script>
