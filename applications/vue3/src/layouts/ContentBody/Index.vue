<template>
  <CCard class="mb-4">
    <CCardHeader>
      <slot name="header">
        <CIcon name="cil-notes" />
        <strong class="pl-1"> {{ $route.name }}</strong>
      </slot>
    </CCardHeader>

    <CCardBody class="pb-5">
      <slot />
    </CCardBody>

    <CCardFooter>
      <slot name="footer"> &nbsp; </slot>
    </CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContentBody',
})
</script>
