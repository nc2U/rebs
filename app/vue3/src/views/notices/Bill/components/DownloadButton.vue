<template>
  <CAlert color="secondary">
    <CButton color="primary" :disabled="disabled">
      선택 건별 고지서 내려받기
    </CButton>
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DownloadButton',
  props: {
    disabled: Boolean,
  },
  methods: {},
})
</script>
