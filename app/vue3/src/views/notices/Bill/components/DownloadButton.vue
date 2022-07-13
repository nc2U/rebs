<template>
  <CAlert color="secondary">
    <CButton color="primary" :disabled="!contractors.length">
      선택 건별 고지서 내려받기
    </CButton>
    {{ contractors }}
  </CAlert>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'DownloadButton',
  props: {
    bill_issue: Object,
    contractors: Array,
  },
  methods: {},
})
</script>
