<template>
  <CCard class="mb-4 text-body">
    <slot name="header">
      <CCardHeader>
        <CIcon name="cil-notes" />
        <strong class="pl-1"> {{ $route.name }}</strong>
      </CCardHeader>
    </slot>

    <slot>
      <CCardBody class="pb-5"> This page is under construction.</CCardBody>

      <CCardFooter>&nbsp;</CCardFooter>
    </slot>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContentBody',
})
</script>
