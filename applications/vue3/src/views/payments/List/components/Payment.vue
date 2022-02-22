<template>
  <CTableRow class="text-center">
    <CTableDataCell>2020-01-01</CTableDataCell>
    <CTableDataCell>1차조합원</CTableDataCell>
    <CTableDataCell>84A</CTableDataCell>
    <CTableDataCell>841001-1</CTableDataCell>
    <CTableDataCell>
      <router-link to="#">김백수</router-link>
    </CTableDataCell>
    <CTableDataCell class="text-right">
      <router-link to="#">15,000,000</router-link>
    </CTableDataCell>
    <CTableDataCell>[계약금] - 3차계약금</CTableDataCell>
    <CTableDataCell>무궁화-분담금(국민)</CTableDataCell>
    <CTableDataCell>김백수906-504</CTableDataCell>
    <CTableDataCell>수정/삭제</CTableDataCell>
  </CTableRow>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Payment',
  props: {
    payment: {
      type: Object,
      required: true,
    },
  },
})
</script>
