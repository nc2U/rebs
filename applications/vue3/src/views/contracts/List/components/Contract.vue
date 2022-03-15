<template>
  <CTableRow v-if="contract" class="text-center">
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
    <CTableDataCell>{{ contract.last_paid_order }}</CTableDataCell>
    <CTableDataCell class="text-right">
      {{ numFormat(contract.total_paid) }}
    </CTableDataCell>
    <CTableDataCell>
      <CBadge :color="contract.is_registed ? 'success' : 'danger'">
        {{ contract.is_registed ? '인가완료' : '미 인 가' }}
      </CBadge>
    </CTableDataCell>
    <CTableDataCell class="text-left">
      {{ cutString(contract.address, 13) }}
    </CTableDataCell>
    <CTableDataCell>{{ contract.cell_phone }}</CTableDataCell>
    <CTableDataCell>{{ contract.contract_date }}</CTableDataCell>
    <CTableDataCell>
      <CButton
        type="button"
        color="success"
        size="sm"
        @click="
          $router.push({
            name: '계약등록 관리',
            query: { contract: contract.pk },
          })
        "
      >
        수정
      </CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import CashesList from '@/views/comCash/Manage/components/CashesList.vue'

export default defineComponent({
  name: 'Contract',
  components: { CashesList },

  props: {
    contract: {
      type: Object,
      required: true,
    },
  },
})
</script>
