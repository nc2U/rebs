<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> {{ $route.name }}</strong>
    </CCardHeader>

    <CCardBody class="pb-5">
      <slot />
    </CCardBody>

    <CCardFooter />&nbsp;
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContentBody',
})
</script>
