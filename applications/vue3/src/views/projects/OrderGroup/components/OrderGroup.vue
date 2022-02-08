<template>
  <CTableRow>
    <CTableDataCell>
      <CFormInput type="number" :value="order.order_number" />
    </CTableDataCell>
    <CTableDataCell>
      <CFormSelect
        :value="order.sort"
        :options="sort"
        :selected="sort.value == order.sort"
      />
    </CTableDataCell>
    <CTableDataCell>
      <CFormInput :value="order.order_group_name" />
    </CTableDataCell>
    <CTableDataCell class="text-center">
      <CButton color="success" size="sm" @click="editing = true">
        수정
      </CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OrderGroup',
  data() {
    return {
      sort: [
        { label: '일반분양', value: '1' },
        { label: '조합모집', value: '2' },
      ],
    }
  },
  props: {
    order: {
      type: Object,
    },
  },
  computed: {},
  methods: {},
})
</script>

<style lang="scss" scoped></style>
