<script lang="ts" setup>
import { onBeforeMount } from 'vue'

const emit = defineEmits(['aside-visible'])

onBeforeMount(() => emit('aside-visible', false))
</script>

<template>
  <CRow class="py-2">
    <CCol>
      <h5>{{ $route.name }}</h5>
    </CCol>
  </CRow>
</template>
