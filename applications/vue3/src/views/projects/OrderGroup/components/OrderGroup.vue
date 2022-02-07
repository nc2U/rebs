<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ order.order_number }}</CTableDataCell>
    <CTableDataCell>{{ order.sort_desc }}</CTableDataCell>
    <CTableDataCell>{{ order.order_group_name }}</CTableDataCell>
    <CTableDataCell>
      <CButton color="success" size="sm">수정</CButton>
      <CButton color="danger" size="sm">삭제</CButton>
    </CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OrderGroup',
  components: {},
  data() {
    return {
      sample: '',
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
