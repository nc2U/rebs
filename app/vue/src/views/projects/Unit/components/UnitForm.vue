<script lang="ts" setup="">
import { ref } from 'vue'

defineProps({ unit: { type: Object, required: true } })

const msg = ref('unit form list')
</script>

<template>
  <CTableRow class="text-center">
    <CTableDataCell>{{ unit.unit_type }}</CTableDataCell>
    <CTableDataCell>{{ unit.floor_type }}</CTableDataCell>
    <CTableDataCell>{{ unit.name }}</CTableDataCell>
    <CTableDataCell>{{ unit.bldg_line }}</CTableDataCell>
    <CTableDataCell>{{ unit.floor_no }}</CTableDataCell>
    <CTableDataCell>{{ unit.is_hold }}</CTableDataCell>
    <CTableDataCell>{{ unit.hold_reason }}</CTableDataCell>
    <CTableDataCell>수정/삭제</CTableDataCell>
  </CTableRow>
</template>
