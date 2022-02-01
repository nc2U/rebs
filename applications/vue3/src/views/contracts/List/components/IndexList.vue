<template>
  <CCard class="mt-4">
    <CCardHeader>
      <CIcon name="cil-notes" />
      <strong class="pl-1"> 계약내역 조회</strong>
    </CCardHeader>

    <CCardBody class="blank-body"></CCardBody>
    <CCardFooter>&nbsp;</CCardFooter>
  </CCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'IndexList',
  components: {},
  data() {
    return {
      sample: '',
    }
  },
  props: {},
  computed: {},
  methods: {},
})
</script>

<style lang="scss" scoped>
.blank-body {
  height: 500px;
}
</style>
