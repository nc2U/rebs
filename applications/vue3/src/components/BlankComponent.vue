<template>
  <CCard class="mb-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> Subpage Title</strong>
    </CCardHeader>

    <CCardBody class="blank-body"></CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'BlankComponent',
  components: {},
})
</script>

<style lang="scss" scoped>
.blank-body {
  height: 460px;
}
</style>
